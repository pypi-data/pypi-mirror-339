import logging
from sqlalchemy.orm import Session
from ceonstock_db import models

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ProductCreate(BaseModel):
    name: str
    description: str
    price_gbp_pence: int


DEFAULT_PRODUCTS = [
    ProductCreate(
        name="video_preview",
        description="Create a watermarked preview video using your custom inputs. Non commercial use.",
        price_gbp_pence=5_00,
    ),
    ProductCreate(
        name="video_hd",
        description="Create a video in HD 1920 x 1080 resolution, using your custom inputs. Includes a Ceon Media Commercial License.",
        price_gbp_pence=250_00,
    ),
    ProductCreate(
        name="video_4k",
        description="Create a video in 4K 3840 x 2160 resolution, using your custom inputs. Includes a Ceon Media Commercial License",
        price_gbp_pence=400_00,
    ),
]


def create_default_products(session: Session):
    logger.info("Adding default products to database...")
    product_sqlalchemy_instances = [
        models.product.ProductTbl(**default_product.__dict__)
        for default_product in DEFAULT_PRODUCTS
    ]
    session.add_all(product_sqlalchemy_instances)
    logger.info("Added default products to session.")
    session.commit()
    logger.info("Committed default products to database.")
