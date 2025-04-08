from typing import Optional

from ...application.services.product_service import ProductService
from ...domain.models.test import TestBase, Test
from ...utils.string import build_query_params, is_valid_id
from ...infrastructure.clients.http_client import Client
from ...utils.s3 import upload_file_to_s3, download_file_from_s3
import os

class TestService:
    def __init__(self, client: Client, product_service: ProductService):
        self._client = client
        self.product_service = product_service

    def __generate_and_upload_presigned_url(self, file_path: str, fileType: str):
        presigned_url_response = self._client.get("s3/generate-put-presigned-url", {
            "key": os.path.basename(file_path),
            "fileType": fileType
        })

        if "uploadPresignedUrl" in presigned_url_response.json():
            presigned_url = presigned_url_response.json().get("uploadPresignedUrl")
        else:
            raise Exception(f"Failed to generate presigned URL")
        
        if not upload_file_to_s3(file_path, presigned_url):
            raise Exception(f"Failed to upload file to {presigned_url}")

        return presigned_url_response.json().get("downloadPresignedUrl")

    def create(self, name: str, type: str, product_id: str, ground_truth_file_path: Optional[str] = None, test_file_path: Optional[str] = None, evolutions: Optional[bool] = False):
        """
        Given a test name, create a new test if it doesn't exist.
        
        Args:
            name (str): Name of the test.
            type (str): Type of the test.

                Possible value is one of the following: `QUALITY`, `RED_TEAMING`.
            product_id (str): Product ID of the test.
            ground_truth_file_path (str, optional): Path to the ground truth file to be uploaded.
            test_file_path (str, optional): Path to the test file to be uploaded.
            evolutions (bool, optional): Whether we should create evolutions in the synthetic data.\n
                Only makes sense for quality testing and tests created by Galtea\n
                Be cautious with this parameter, as it will create more test cases and be more expensive.
            
        Returns:
            Test: The created test object.
        """
        ground_truth_url = self.__generate_and_upload_presigned_url(ground_truth_file_path, "groundTruth") if ground_truth_file_path else None
        test_presigned_url = self.__generate_and_upload_presigned_url(test_file_path, "testFile") if test_file_path else None

        test = TestBase(
            name=name,
            type=type,
            evolutions=evolutions,
            product_id=product_id,
            ground_truth_uri=ground_truth_url,
            uri=test_presigned_url
        )
        test.model_validate(test.model_dump())

        response = self._client.post("tests", json=test.model_dump(by_alias=True))
        test_response = Test(**response.json())

        return test_response

    def get(self, test_id: str):
        """
        Retrieve a test by its ID.
        
        Args:
            test_id (str): ID of the test to retrieve.
            
        Returns:
            Test: The retrieved test object.
        """
        if not is_valid_id(test_id):
            raise ValueError("Test ID provided is not valid.")
        
        response = self._client.get(f"tests/{test_id}")
        return Test(**response.json())
    
    def get_by_name(self, product_id: str, test_name: str, type: Optional[str] = None):
        """
        Retrieve a test by its name and the product ID it is assiacted with.
        
        Args:
            product_id (str): ID of the product.
            test_name (str): Name of the test to retrieve.
            type (str, optional): Type of the test, this is needed when there is a test with the same name for both types.

                Possible value is one of the following: `QUALITY`, `RED_TEAMING`.
            
        Returns:
            Test: The retrieved test object.
        """
        if not is_valid_id(product_id):
            raise ValueError("Product ID provided is not valid.")

        query_params = build_query_params(productIds=[product_id], names=[test_name], types=[type.upper()] if type else None)
        response = self._client.get(f"tests?{query_params}")
        tests = [Test(**test) for test in response.json()]

        if not tests:
            try:
                self.product_service.get(product_id)
            except:
                raise ValueError(f"Product with ID {product_id} does not exist.")

        if not tests:
            raise ValueError(f"Test with name {test_name} does not exist.")
        
        if len(tests) > 1:
            raise ValueError(f"Multiple tests with name {test_name} exist, please specify the type parameter.")

        return tests[0]

    def download(self, test: Test, output_directory: str):
        """
        Download a test file from S3 using the presigned URL.
        
        Args:
            test (Test): Test object.
            output_directory (str): Directory where the file will be downloaded.
            
        Returns:
            str: Path to the downloaded file.
        """
        query_params = build_query_params(s3Uri=test.uri)
        response = self._client.get(f"s3/generate-get-presigned-url?{query_params}")
        if "downloadPresignedUrl" in response.json():
            download_url = response.json().get("downloadPresignedUrl")
        else:
            raise Exception(f"Failed to generate download URL")
        
        return download_file_from_s3(download_url, os.path.basename(test.uri), output_directory)

    def list(self, product_id: str, offset: Optional[int] = None, limit: Optional[int] = None):
        """
        List all tests for a given product.
        
        Args:
            product_id (str): ID of the product.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            list[Test]: List of test objects.
        """
        if not is_valid_id(product_id):
            raise ValueError("Product ID provided is not valid.")
        
        query_params = build_query_params(productIds=[product_id], offset=offset, limit=limit)
        response = self._client.get(f"tests?{query_params}")
        tests = [Test(**test) for test in response.json()]
        
        if not tests:
            try:
                self.product_service.get(product_id)
            except:
                raise ValueError(f"Product with ID {product_id} does not exist.")
            
        return tests

    def delete(self, test_id: str):
        """
        Delete a test by its ID.
        
        Args:
            test_id (str): ID of the test to delete.
            
        Returns:
            Test: Deleted test object.
        """
        if not is_valid_id(test_id):
            raise ValueError("Test ID provided is not valid.")
        
        self._client.delete(f"tests/{test_id}")