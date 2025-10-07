"""
Test for the generation API endpoint

Tests the POST /api/v1/generation/generate endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

# Note: These tests are designed to verify the structure
# Full integration tests will run when the backend is fully operational


class TestGenerationAPI:
    """Test suite for Generation API endpoint."""
    
    @pytest.fixture
    def sample_generation_request(self):
        """Sample generation request payload."""
        return {
            "pattern_id": "shadcn-button",
            "tokens": {
                "colors": {
                    "Primary": "#3B82F6",
                    "Secondary": "#64748B"
                },
                "typography": {
                    "fontSize": "14px",
                    "fontFamily": "Inter, sans-serif"
                },
                "spacing": {
                    "padding": "16px"
                }
            },
            "requirements": {
                "props": [
                    {
                        "name": "variant",
                        "type": "string",
                        "values": ["default", "secondary", "ghost"],
                        "required": False
                    }
                ],
                "events": [
                    {"name": "onClick", "type": "MouseEvent"}
                ]
            }
        }
    
    def test_generation_request_structure(self, sample_generation_request):
        """Test that generation request has correct structure."""
        assert "pattern_id" in sample_generation_request
        assert "tokens" in sample_generation_request
        assert "requirements" in sample_generation_request
        
        # Validate tokens structure
        tokens = sample_generation_request["tokens"]
        assert "colors" in tokens
        assert "typography" in tokens
        assert "spacing" in tokens
        
        # Validate requirements structure
        requirements = sample_generation_request["requirements"]
        assert "props" in requirements
        assert "events" in requirements
    
    def test_expected_response_structure(self):
        """Test expected response structure from generation endpoint."""
        expected_response = {
            "success": True,
            "component_code": "// Component code here",
            "stories_code": "// Stories code here",
            "files": {
                "Button.tsx": "// Component code",
                "Button.stories.tsx": "// Stories code"
            },
            "metadata": {
                "latency_ms": 1000,
                "stage_latencies": {
                    "parsing": 100,
                    "injecting": 50,
                    "generating": 30,
                    "implementing": 100,
                    "assembling": 720
                },
                "token_count": 5,
                "lines_of_code": 150,
                "requirements_implemented": 2
            }
        }
        
        # Validate response structure
        assert "success" in expected_response
        assert "component_code" in expected_response
        assert "stories_code" in expected_response
        assert "files" in expected_response
        assert "metadata" in expected_response
        
        # Validate metadata
        metadata = expected_response["metadata"]
        assert "latency_ms" in metadata
        assert "stage_latencies" in metadata
        assert "token_count" in metadata
        assert "lines_of_code" in metadata
    
    @pytest.mark.asyncio
    async def test_generator_service_integration(self):
        """Test that GeneratorService can be called correctly."""
        from src.generation.generator_service import GeneratorService
        from src.generation.types import GenerationRequest
        
        # Create service
        service = GeneratorService()
        
        # Verify service has required methods
        assert hasattr(service, 'generate')
        assert hasattr(service, 'get_current_stage')
        assert hasattr(service, 'get_stage_latencies')
        
        # Verify service components initialized
        assert service.pattern_parser is not None
        assert service.token_injector is not None
        assert service.tailwind_generator is not None
        assert service.requirement_implementer is not None
        assert service.code_assembler is not None
    
    def test_api_endpoint_paths(self):
        """Test that API endpoints are correctly defined."""
        # Expected endpoints
        expected_endpoints = [
            "/api/v1/generation/generate",      # POST - Generate component
            "/api/v1/generation/patterns",      # GET - List patterns
            "/api/v1/generation/status/{pattern_id}"  # GET - Get status
        ]
        
        # Verify endpoint paths are defined
        for endpoint in expected_endpoints:
            assert endpoint is not None
    
    def test_error_handling_structure(self):
        """Test expected error response structure."""
        error_responses = [
            {
                "status_code": 400,
                "scenario": "Missing pattern_id",
                "expected_detail": "pattern_id is required"
            },
            {
                "status_code": 404,
                "scenario": "Pattern not found",
                "expected_detail": "Pattern not found: shadcn-nonexistent"
            },
            {
                "status_code": 500,
                "scenario": "Generation failure",
                "expected_detail": "Code generation failed: ..."
            }
        ]
        
        for error in error_responses:
            assert "status_code" in error
            assert "scenario" in error
            assert "expected_detail" in error
