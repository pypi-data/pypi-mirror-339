from arrc.layers import RescaleToRange, OptimizedRandomShiftAugmentation, RandomAmpScalingAugmentation, \
    RandomAdditiveNoise


def get_augmented_input(inputs,
                        add_noise=True,
                        random_shift=True,
                        random_amp_scaling=True):
    x = inputs

    if random_amp_scaling:
        x = RandomAmpScalingAugmentation(min_scale=0.97, max_scale=1.03, likelihood=0.1)(x)

    if random_shift:
        x = OptimizedRandomShiftAugmentation(max_shift=0.1, likelihood=0.1)(x)

    if add_noise:
        x = RandomAdditiveNoise(0.01, likelihood=0.1)(x)

    x = RescaleToRange(new_min=-5, new_max=5)(x)

    return x