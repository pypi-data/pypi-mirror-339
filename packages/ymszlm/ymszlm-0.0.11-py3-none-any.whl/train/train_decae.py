import argparse
import os

import torch
from torch.nn import MSELoss
from torch.optim.lr_scheduler import ReduceLROnPlateau

from models.HSAZLM import DRCAE
from tools.dataset import create_dataloaders
from tools.plotting import plot_all_metrics
from tools.tool import initialize_results_file, append_to_results_file
from tools.train_eval_utils import train_decae_one_epoch


def main(args):
    save_dir = args.save_dir
    img_dir = os.path.join(save_dir, 'images')
    model_dir = os.path.join(save_dir, 'models')

    results_file = os.path.join(save_dir, 'decae_results.txt')
    decae_column_order = ['epoch', 'train_losses', 'val_losses', 'lrs']
    initialize_results_file(results_file, decae_column_order)
    custom_column_widths = {'epoch': 5, 'train_loss': 12, 'val_loss': 10, 'lr': 3}

    device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
    print("Using {} device training.".format(device.type))

    train_loader, val_loader = create_dataloaders(args.data_dir, args.batch_size)
    metrics = {'train_losses': [], 'val_losses': [], 'lrs': []}

    model = DRCAE().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    lr_scheduler = ReduceLROnPlateau(optimizer, 'min', factor=0.1, patience=4, min_lr=1e-9)
    criterion = MSELoss()
    best = 1e8
    for epoch in range(0, args.epochs):
        result = train_decae_one_epoch(model, train_loader, val_loader, device, optimizer, criterion, epoch)
        lr = lr_scheduler.get_last_lr()[0]
        lr_scheduler.step(result['val_loss'])

        metrics['val_losses'].append(result['val_loss'])
        metrics['train_losses'].append(result['train_loss'])
        metrics['lrs'].append(lr)
        result.update({'lr': lr})

        append_to_results_file(results_file, result, decae_column_order,
                               custom_column_widths=custom_column_widths)

        save_file = {
            'epoch': epoch,
            'model_state_dict': model,
            'optimizer_state_dict': optimizer,
            'lr_scheduler_state_dict': lr_scheduler,
        }
        torch.save(save_file, os.path.join(model_dir, 'last_decae.pt'))
        if result['val_loss'] < best:
            best = result['val_loss']
            model.save(os.path.join(model_dir, 'decae.pt'))

    plot_all_metrics(metrics, args.epochs, 'decae', img_dir)
    os.remove(os.path.join(model_dir, 'last_decae.pt'))


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default=r'/data/coding/data/D0')
    parser.add_argument('--save_dir', type=str, default='/data/coding/results/train_D0')
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--batch_size', type=int, default=64)
    return parser.parse_args(args if args else [])


if __name__ == '__main__':
    opts = parse_args()
    print(opts)
    main(opts)
