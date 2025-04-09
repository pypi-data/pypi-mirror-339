"""tests for vak.config.train module"""
import pytest

import torchbiosound.config.train


class TestTrainConfig:

    @pytest.mark.parametrize(
            'config_dict',
            [
                {
                    'standardize_frames': True,
                    'batch_size': 11,
                    'num_epochs': 2,
                    'val_step': 50,
                    'ckpt_step': 200,
                    'patience': 4,
                    'num_workers': 16,
                    'trainer': {'accelerator': 'gpu', 'devices': [0]},
                    'root_results_dir': './tests/data_for_tests/generated/results/train/audio_cbin_annot_notmat/TweetyNet',
                    'model': {
                        'TweetyNet': {
                            'network': {
                                'conv1_filters': 8,
                                'conv1_kernel_size': [3, 3],
                                'conv2_filters': 16,
                                'conv2_kernel_size': [5, 5],
                                'pool1_size': [4, 1],
                                'pool1_stride': [4, 1],
                                'pool2_size': [4, 1],
                                'pool2_stride': [4, 1],
                                'hidden_size': 32
                            },
                            'optimizer': {
                                'lr': 0.001
                            }
                        }
                    },
                    'dataset': {
                        'path': 'tests/data_for_tests/generated/prep/train/audio_cbin_annot_notmat/TweetyNet/032312-vak-frame-classification-dataset-generated-240502_234819'
                    }
                }
            ]
    )
    def test_init(self, config_dict):
        config_dict['model'] = torchbiosound.config.ModelConfig.from_config_dict(config_dict['model'])
        config_dict['dataset'] = torchbiosound.config.DatasetConfig.from_config_dict(config_dict['dataset'])
        config_dict['trainer'] = torchbiosound.config.TrainerConfig(**config_dict['trainer'])

        train_config = torchbiosound.config.TrainConfig(**config_dict)

        assert isinstance(train_config, torchbiosound.config.TrainConfig)

    @pytest.mark.parametrize(
            'config_dict',
            [
                {
                    'standardize_frames': True,
                    'batch_size': 11,
                    'num_epochs': 2,
                    'val_step': 50,
                    'ckpt_step': 200,
                    'patience': 4,
                    'num_workers': 16,
                    'trainer': {'accelerator': 'gpu', 'devices': [0]},
                    'root_results_dir': './tests/data_for_tests/generated/results/train/audio_cbin_annot_notmat/TweetyNet',
                    'model': {
                        'TweetyNet': {
                            'network': {
                                'conv1_filters': 8,
                                'conv1_kernel_size': [3, 3],
                                'conv2_filters': 16,
                                'conv2_kernel_size': [5, 5],
                                'pool1_size': [4, 1],
                                'pool1_stride': [4, 1],
                                'pool2_size': [4, 1],
                                'pool2_stride': [4, 1],
                                'hidden_size': 32
                            },
                            'optimizer': {
                                'lr': 0.001
                            }
                        }
                    },
                    'dataset': {
                        'path': 'tests/data_for_tests/generated/prep/train/audio_cbin_annot_notmat/TweetyNet/032312-vak-frame-classification-dataset-generated-240502_234819'
                    }
                }
            ]
    )
    def test_from_config_dict(self, config_dict):
        train_config = torchbiosound.config.TrainConfig.from_config_dict(config_dict)

        assert isinstance(train_config, torchbiosound.config.TrainConfig)

    def test_from_config_dict_with_real_config(self, a_generated_train_config_dict):
        train_table = a_generated_train_config_dict["train"]

        train_config = torchbiosound.config.train.TrainConfig.from_config_dict(train_table)

        assert isinstance(train_config, torchbiosound.config.train.TrainConfig)

    @pytest.mark.parametrize(
            'config_dict, expected_exception',
            [
                (
                    {
                        'standardize_frames': True,
                        'batch_size': 11,
                        'num_epochs': 2,
                        'val_step': 50,
                        'ckpt_step': 200,
                        'patience': 4,
                        'num_workers': 16,
                        'trainer': {'accelerator': 'gpu', 'devices': [0]},
                        'root_results_dir': './tests/data_for_tests/generated/results/train/audio_cbin_annot_notmat/TweetyNet',
                        'dataset': {
                            'path': 'tests/data_for_tests/generated/prep/train/audio_cbin_annot_notmat/TweetyNet/032312-vak-frame-classification-dataset-generated-240502_234819'
                        }
                    },
                    KeyError
                ),
                (
                    {
                        'standardize_frames': True,
                        'batch_size': 11,
                        'num_epochs': 2,
                        'val_step': 50,
                        'ckpt_step': 200,
                        'patience': 4,
                        'num_workers': 16,
                        'trainer': {'accelerator': 'gpu', 'devices': [0]},
                        'root_results_dir': './tests/data_for_tests/generated/results/train/audio_cbin_annot_notmat/TweetyNet',
                        'model': {
                            'TweetyNet': {
                                'network': {
                                    'conv1_filters': 8,
                                    'conv1_kernel_size': [3, 3],
                                    'conv2_filters': 16,
                                    'conv2_kernel_size': [5, 5],
                                    'pool1_size': [4, 1],
                                    'pool1_stride': [4, 1],
                                    'pool2_size': [4, 1],
                                    'pool2_stride': [4, 1],
                                    'hidden_size': 32
                                },
                                'optimizer': {
                                    'lr': 0.001
                                }
                            }
                        },
                    },
                    KeyError
                )
            ]
    )
    def test_from_config_dict_raises(self, config_dict, expected_exception):
        with pytest.raises(expected_exception):
            torchbiosound.config.TrainConfig.from_config_dict(config_dict)
