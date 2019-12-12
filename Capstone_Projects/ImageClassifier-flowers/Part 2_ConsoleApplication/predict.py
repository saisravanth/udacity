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

parser = argparse.ArgumentParser(description='Provides Inference from a trained Neural Net')
parser.add_argument('indir', type=str, help='Input dir for Neural Net: str')
parser.add_argument('checkpoint', default='trained_checkpoint', type=str, help='Checkpoint dir to fetch the trained Neural Net: str')
parser.add_argument('--top_k', default=5, type=int, help='Choose top_K most likely: int')
parser.add_argument('--gpu', default=True, type=toBool, help='Choose to run on gpu: bool')

args = parser.parse_args()

utility_obj = Utility()
model_obj = Model()
model = model_obj.load_model(args.checkpoint, args.gpu)

probs, classes = model_obj.predict(args.indir, model, args.gpu, args.top_k)
cat_to_name = utility_obj.get_cat_to_name()
flowers = [cat_to_name[i] for i in classes]
print("Probability: ",probs)
print("Flower class: ", flowers)





# print(args.indir)
# print(args.checkpoint)
# print(args.top_k)
# print(args.gpu)