import pygame.rect
from settings import *

def folder_importer(*path):
    """Imports images from the folder of the custom path."""

    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs


def audio_importer(*path):
    """Imports audio from the folder of the custom parts."""

    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict


def tile_importer(cols, *path):
    """Imports animation frames .png tile and cuts it into individual frames."""

    attack_frames = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            attack_frames[file_name.split('.')[0]] = []
            cutout_w = surf.get_width() / cols
            for col in range(cols):
                cutout_surf = pygame.Surface((cutout_w, surf.get_height()), pygame.SRCALPHA)
                cutout_rect = pygame.rect.FRect(cutout_w * col, 0,cutout_w, surf.get_height())
                cutout_surf.blit(surf, (0,0), cutout_rect)
                attack_frames[file_name.split('.')[0]].append(cutout_surf)
    return attack_frames