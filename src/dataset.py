from datasets import load_dataset
from dotenv import load_dotenv
from src.config import DATASET_NAME

load_dotenv()

dataset = load_dataset(
  DATASET_NAME,
)

profiles = dataset["train"]

# Original OkCupid essay prompts.
ESSAY_PROMPTS = {
  "essay0": "About me",
  "essay1": "What I'm doing with my life",
  "essay2": "Things I'm good at",
  "essay3": "What people first notice about me",
  "essay4": "Favorite books, movies, shows, music, and food",
  "essay5": "Things I couldn't live without",
  "essay6": "Things I spend time thinking about",
  "essay7": "What I do on a typical Friday night",
  "essay8": "Something personal about me",
  "essay9": "Who should message me",
}