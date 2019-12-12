import argparse
from model import Model
from utility import Utility

def toBool(a):
    if isinstance(a, bool):
       return a
    if a.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif a.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Please provide boolean type')

parser = argparse.ArgumentParser(description='Train a  VGG Neural Net')
parser.add_argument('indir', type=str, help='Input dir for Neural Net: str')
parser.add_argument('--save_dir', default='trained_checkpoint', type=str, help='Checkpoint dir to save trained Neural Net: str')
parser.add_argument('--arch', default='VGG16', type=str, help='Choose architecture VGG16 or VGG19: str')
parser.add_argument('--learning_rate', default=0.00025, type=float, help='Choose learning rate: float')
parser.add_argument('--epochs', default=10, type=int, help='Choose epochs to train: int')
parser.add_argument('--gpu', default=True, type=toBool, help='Choose to run on gpu: bool')

args = parser.parse_args()

utility_obj = Utility()
transform, transform_basic = utility_obj.get_transforms()
loaders = utility_obj.get_dataLoaders(transform, transform_basic, args.indir)

model_obj = Model()
model = model_obj.createModel(args.arch, args.gpu)
criterion, optimizer = model_obj.get_criterion_optimizer(model, args.learning_rate, momentum=0.9)
model = model_obj.train(args.epochs, loaders, model, args.arch, optimizer, criterion, args.gpu, args.save_dir)






# print(args.indir)
# print(args.save_dir)
# print(args.arch)
# print(args.learning_rate)
# print(args.epochs)
# print(args.gpu)