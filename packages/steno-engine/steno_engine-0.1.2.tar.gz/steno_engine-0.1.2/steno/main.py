import time
import sys
# local imports
from .simplify import compress_text
from .token_metrics import summary
from .log import logger


def cli():

    sample_text = """
    This is a sample text that we will use to test the compression function.
    It contains multiple sentences and some complex structures.
    <literal>here be the dragons</literal>
    The goal is to simplify it while preserving the meaning.
"""
    sample_text = """
Here is a product FAQ document for our customer support reps:

Q: What is the return policy?
A: Customers have 30 days from the date of delivery to return an item. The item must be unused and in its original packaging.

Q: Do you offer free shipping?
A: Yes, free standard shipping is available on orders over $50 within the contiguous United States.

Q: How do I track my order?
A: Once your order ships, you will receive an email with a tracking link. You can also check your order status under "My Orders" in your account.


Please read the FAQ and write a concise summary that a customer support agent could use in conversation.
"""
    # sample_text = "You crossed the line. People trusted you and they died. You gotta go down."
    sample_text2 = """
Yeah <literal>(You can't touch this)</literal>
Look, man <literal>(You can't touch this)</literal>
You better get hype, boy, because you know you can't <literal>(You can't touch this)</literal>
"""

    start_time = time.time()
    result = compress_text(sample_text)
    end_time = time.time()
    logger.info(sample_text)
    print('-'*80)
    logger.info(summary(sample_text, result))
    logger.info(f"Compression took {(end_time - start_time) * 1000:.2f} ms")
    sys.stdout.write(result + '\n')


def download():
    from .simplify import load_spacy_model
    from .execute import ModelRunner

    load_spacy_model()  # download spacy model if not already present
    _ = ModelRunner()  # triggers lazy model download
    print("✅ All models downloaded.")


if __name__ == "__main__":
    cli()
