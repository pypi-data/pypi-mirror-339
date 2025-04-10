import os
from torch.utils.data import Dataset
import torch


class LibriBrainCompetitionHoldout(Dataset):

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.features = torch.load(os.path.join(data_path, "data.pt"))
        self.labels = torch.load(os.path.join(data_path, "labels.pt"))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


if __name__ == "__main__":
    dataset = LibriBrainCompetitionHoldout(
        "/Users/mirgan/LibriBrain/competitionShuffled/"
    )
    print(len(dataset))
    print(dataset[0])
    print(dataset[1])
