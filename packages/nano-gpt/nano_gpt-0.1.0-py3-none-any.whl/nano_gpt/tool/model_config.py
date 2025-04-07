"""Shared library for command line flags for loading models.

This module provides functions for creating and parsing command line arguments for
loading models, as well as functions for converting these arguments into model
configurations.

This can be used to load a model from a checkpoint, a pretrained model, or
initialize a model from pre-defined model configuration from the GPT-2 paper.
"""

from argparse import ArgumentParser, BooleanOptionalAction
from collections.abc import Generator
from contextlib import contextmanager
import dataclasses
import json
import logging
import pathlib
from typing import Any, cast

import torch
from huggingface_hub import HfFileSystem

from nano_gpt.checkpoint import load_checkpoint, Checkpoint
from nano_gpt.config import (
    MODELS,
    config_from,
    TrainedModelConfig,
    EvalConfig,
    SampleConfig,
    DatasetConfig,
    model_config_from_pretrained,
    model_config_from_dict,
)
from nano_gpt.datasets import TRAIN_DATASETS
from nano_gpt.devices import get_device
from nano_gpt.model import GPT
from nano_gpt.tokenizer import get_tokenizer, Tokenizer

_LOGGER = logging.getLogger(__name__)

DATASET_DIR = "dataset_cache"


def create_model_arguments(
    args: ArgumentParser, default_values: dict[str, Any] | None = None
) -> None:
    """Create arguments for model loading."""
    if default_values is None:
        default_values = {}
    group = args.add_argument_group("model")
    group.add_argument(
        "--pretrained",
        type=str,
        help="The name of the pretrained model to use.",
    )
    group.add_argument(
        "--model",
        type=str,
        default=default_values.get("model", "gpt2"),
        choices=sorted(MODELS),
        help="Use the specified model name configuration default values.",
    )
    group.add_argument(
        "--checkpoint",
        type=str,
        help="Load a model from a checkpoint.",
    )
    group.add_argument(
        "--device",
        type=str,
        help="The device to use.",
    )
    group.add_argument(
        "--sequence-length",
        type=int,
        help="The sequence length used for input content in each micro batch.",
    )
    group.add_argument(
        "--seed",
        type=int,
        help="The seed to use for sampling/training.",
    )
    group.add_argument(
        "--compile",
        type=str,
        action=BooleanOptionalAction,
        default=True,
        help="Will compile the model if supported by the device.",
    )


def _check_model_arguments(args: Any) -> None:
    """Check that the model arguments are valid."""
    if args.pretrained is None and args.checkpoint is None and args.model is None:
        raise ValueError(
            "Either --pretrained or --checkpoint or --model must be specified"
        )


def model_config_from_args(
    args: Any,
) -> TrainedModelConfig:
    """Create a model from the flags."""
    return config_from(
        args.model,
        **{
            key: value
            for key in {"micro_batch_size", "sequence_length", "total_batch_size"}
            if (value := getattr(args, key, None)) is not None
        },
    )


@contextmanager
def load_checkpoint_context(args: Any) -> Generator[Checkpoint | None, None, None]:
    """Load a checkpoint from the flags.

    This is a context manager so that the checkpoint can be used across multiple calls to
    parse arguments, but then discarded after the checkpoint is no longer needed.
    """
    if args.checkpoint is not None:
        checkpoint_path = pathlib.Path(args.checkpoint)
        _LOGGER.info("Restoring from checkpoint: %s", checkpoint_path)
        yield load_checkpoint(checkpoint_path, args.device)
    else:
        yield None


def _trained_model_config_dict_from_args(args: Any) -> dict[str, Any]:
    """Create a TrainedModelConfig parameter dict from flags."""
    return {
        key: value
        for key in {
            "seed",
            "micro_batch_size",
            "sequence_length",
            "total_batch_size",
            "max_steps",
            "eval_steps",
            "eval_num_samples",
            "checkpoint_steps",
            "checkpoint_dir",
            "log_file",
        }
        if (value := getattr(args, key, None)) is not None
    }


def model_from_args(
    args: Any, checkpoint: Checkpoint | None
) -> tuple[GPT, Tokenizer, TrainedModelConfig | None]:
    """Create a model from the flags."""
    _check_model_arguments(args)
    tokenizer = get_tokenizer()
    trained_model_config: TrainedModelConfig | None = None
    if args.pretrained is not None:
        if checkpoint is not None:
            raise ValueError("Cannot specify both --pretrained and --checkpoint")
        _LOGGER.info("loading weights from pretrained gpt: %s" % args.pretrained)
        pretrained_args: dict[str, Any] = {}
        if args.pretrained.startswith("./") or args.pretrained.startswith("/"):
            # If the pretrained model is a local path, we need to load it from the local
            local_path = pathlib.Path(args.pretrained)
            model_config_path = local_path / "config.json"
            _LOGGER.info("Loading model config from %s", model_config_path)
            data = json.loads(model_config_path.read_text())
            model_config = model_config_from_dict(data)
        elif args.pretrained in MODELS:
            _LOGGER.info("Loading known model config: %s", args.pretrained)
            model_config = model_config_from_pretrained(args.pretrained)
        else:
            fs = HfFileSystem()
            model_config_path = pathlib.Path(args.pretrained) / "/config.json"
            _LOGGER.info("Loading model config from %s", model_config_path)
            data = json.loads(fs.read_text(str(model_config_path)))
            model_config = model_config_from_dict(data)
        _LOGGER.info("Initializing model from pretrained config: %s", model_config)
        model = GPT.from_pretrained(
            args.pretrained,
            tokenizer=tokenizer,
            model_config=model_config,
            **pretrained_args,
        )
    elif checkpoint is not None:
        _LOGGER.debug("initializing model from checkpoint: %s", checkpoint.config)
        model = GPT(checkpoint.config, tokenizer=tokenizer)
        model.load_state_dict(checkpoint.model_state_dict_for_inference)
        model_config = checkpoint.config
        train_config = dataclasses.replace(
            checkpoint.train_config,
            **_trained_model_config_dict_from_args(args),
        )
        trained_model_config = TrainedModelConfig(
            model_name=checkpoint.name or "checkpoint",
            model_config=checkpoint.config,
            train_config=train_config,
        )
    else:
        trained_model_config = config_from(
            args.model,
            **_trained_model_config_dict_from_args(args),
        )
        model_config = trained_model_config.model_config
        _LOGGER.debug("initializing model from config: %s", model_config)
        model = GPT(model_config, tokenizer=tokenizer)
    _LOGGER.info("Trained model config: %s", trained_model_config)
    if args.device is None:
        args.device = get_device()
    # TODO: Fix compilation with DDP
    if args.device == "cuda":
        if args.compile:
            _LOGGER.info("Compiling model")
            try:
                model = cast(GPT, torch.compile(model))
            except RuntimeError as err:
                raise RuntimeError(
                    f"Failed to compile model, try with --no-compile: {err}"
                ) from err
        else:
            _LOGGER.debug("Not compiling model")
    else:
        _LOGGER.debug("Model will not be compiled (%s)", args.device)

    seed: int | None = None
    if (
        trained_model_config is not None
        and trained_model_config.train_config.seed is not None
    ):
        seed = trained_model_config.train_config.seed
    if args.seed is not None:
        seed = args.seed

    if seed is not None:
        _LOGGER.info("Setting seed to %s", seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)

    return model, tokenizer, trained_model_config


def create_eval_arguments(args: ArgumentParser) -> None:
    """Create arguments for model evaluation."""
    group = args.add_argument_group("eval")
    group.add_argument(
        "--validation-steps",
        type=int,
        help="Number of validation loss iterations to perform each eval round.",
    )
    group.add_argument(
        "--hellaswag-samples",
        type=int,
        help="The number of HellaSwag evaluation results to sample or None for the entire set.",
    )


def eval_config_from_args(args: Any, checkpoint: Checkpoint | None) -> EvalConfig:
    """Create an EvalConfig from the flags."""
    values = {}
    if args.validation_steps is not None:
        values["validation_steps"] = args.validation_steps
    if args.hellaswag_samples is not None:
        values["hellaswag_samples"] = args.hellaswag_samples
    if checkpoint is not None and checkpoint.eval_config is not None:
        return dataclasses.replace(
            checkpoint.eval_config,
            **values,
        )
    return EvalConfig(**values)


def create_sample_arguments(args: ArgumentParser) -> None:
    """Create arguments for model sampling."""
    group = args.add_argument_group("sample")
    group.add_argument(
        "--sample-num-sequences",
        type=int,
        help="The number of sequences to generate.",
    )
    group.add_argument(
        "--sample-max-length",
        type=int,
        help="The maximum length of the generated sequences.",
    )
    group.add_argument(
        "--sample-seed",
        type=int,
        help="The seed to use for sampling.",
    )


def sample_config_from_args(args: Any, checkpoint: Checkpoint | None) -> SampleConfig:
    """Create an SampleConfig from the flags."""
    values = {}
    if args.sample_num_sequences is not None:
        values["num_return_sequences"] = args.sample_num_sequences
    if args.sample_max_length is not None:
        values["max_length"] = args.sample_max_length
    if args.sample_seed is not None:
        values["seed"] = args.sample_seed
    if checkpoint is not None and checkpoint.sample_config is not None:
        return dataclasses.replace(
            checkpoint.sample_config,
            **values,
        )
    return SampleConfig(**values)


def create_dataset_arguments(args: ArgumentParser) -> None:
    """Create arguments for dataset loading."""
    group = args.add_argument_group("dataset")
    group.add_argument(
        "--dataset",
        type=str,
        help="Use the specified dataset.",
        choices=TRAIN_DATASETS.keys(),
        required=False,
    )
    group.add_argument(
        "--dataset-dir",
        type=str,
        help="Directory where the dataset is stored.",
        default=DATASET_DIR,
    )
    args.add_argument(
        "--micro-batch-size",
        type=int,
        help="The number of batches of examples to pull from the dataset in each micro step.",
    )


def dataset_config_from_args(args: Any, checkpoint: Checkpoint | None) -> DatasetConfig:
    """Create a DatasetConfig from the flags."""
    values = {}
    if args.dataset is not None:
        values["dataset_name"] = args.dataset
    if args.dataset_dir is not None:
        values["dataset_dir"] = args.dataset_dir
    if args.micro_batch_size is not None:
        values["micro_batch_size"] = args.micro_batch_size
    if args.sequence_length is not None:
        values["sequence_length"] = args.sequence_length
    if checkpoint is not None and checkpoint.dataset_config is not None:
        return dataclasses.replace(
            checkpoint.dataset_config,
            **values,
        )
    return DatasetConfig(**values)
