import torch
from scipy.io import savemat

from tools.dataset import create_dataloaders
from train.semantics import cnn_extract_features

device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
print(device)
feature_extractor = torch.load(r'D:\Code\2-ZSL\1-output\2-results\train_D2\models\feature_extractor.pt',
                               map_location='cpu', weights_only=False).to(device)
train_loader, val_loader = create_dataloaders(r'D:\Code\2-ZSL\Zero-Shot-Learning\data\data\dataset\CRWU\D2',
                                              128, train_shuffle=False)
train_features, train_labels = cnn_extract_features(feature_extractor, train_loader, device)
val_features, val_labels = cnn_extract_features(feature_extractor, val_loader, device)
savemat(r'D:\Code\2-ZSL\1-output\2-results\train_D2\D2-D2.mat', {'train_features': train_features,
                                                                 'train_labels': train_labels,
                                                                 'val_features': val_features, 'val_labels': val_labels,
                                                                 'class': train_loader.dataset.classes})
