from typing import Optional

from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class TestBase(FromCamelCaseBaseModel):
    product_id: str
    name: str
    type: str
    evolutions: Optional[bool] = False
    ground_truth_uri: Optional[str] = None
    uri: Optional[str] = None

class Test(TestBase):
    id: str
    created_at: str
    deleted_at: Optional[str] = None