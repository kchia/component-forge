#!/usr/bin/env python3
"""Calculate API costs for token extraction based on usage patterns."""

import argparse
from typing import Dict, Tuple


# GPT-4o Pricing (as of 2024 - verify at https://openai.com/api/pricing/)
INPUT_COST_PER_1M_TOKENS = 2.50  # $2.50 per 1M input tokens
OUTPUT_COST_PER_1M_TOKENS = 10.00  # $10.00 per 1M output tokens

# Token estimates
PROMPT_TOKENS = 500  # ~2,000 characters in prompt
AVERAGE_OUTPUT_TOKENS = 1000  # Typical JSON response size


def estimate_image_tokens(width: int, height: int, detail: str = "high") -> int:
    """Estimate image tokens based on dimensions.
    
    For GPT-4o with detail="high":
    - Images are processed at higher resolution
    - Formula: (width * height) / 512^2 * 170 (approximate)
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        detail: Image detail level ("high" or "low")
        
    Returns:
        Estimated number of tokens
    """
    pixels = width * height
    
    if detail == "high":
        # High detail: more tokens per pixel
        # Base formula: tiles of 512x512, each tile costs ~170 tokens
        tiles = (pixels / (512 * 512))
        tokens = int(tiles * 170)
        # Minimum cost for any image
        return max(tokens, 85)  # Minimum ~85 tokens
    else:
        # Low detail: fixed cost
        return 85


def calculate_single_extraction_cost(
    image_width: int = 1920,
    image_height: int = 1080,
    output_tokens: int = None,
    detail: str = "high"
) -> Dict[str, float]:
    """Calculate cost for a single token extraction.
    
    Args:
        image_width: Width of the image in pixels
        image_height: Height of the image in pixels
        output_tokens: Number of output tokens (defaults to average)
        detail: Image detail level
        
    Returns:
        Dictionary with cost breakdown
    """
    if output_tokens is None:
        output_tokens = AVERAGE_OUTPUT_TOKENS
    
    # Calculate tokens
    text_input_tokens = PROMPT_TOKENS
    image_input_tokens = estimate_image_tokens(image_width, image_height, detail)
    total_input_tokens = text_input_tokens + image_input_tokens
    
    # Calculate costs
    input_cost = (total_input_tokens / 1_000_000) * INPUT_COST_PER_1M_TOKENS
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M_TOKENS
    total_cost = input_cost + output_cost
    
    return {
        "text_input_tokens": text_input_tokens,
        "image_input_tokens": image_input_tokens,
        "total_input_tokens": total_input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def calculate_monthly_cost(
    extractions_per_month: int,
    avg_image_width: int = 1920,
    avg_image_height: int = 1080,
    detail: str = "high"
) -> Dict[str, float]:
    """Calculate monthly cost based on usage.
    
    Args:
        extractions_per_month: Number of extractions per month
        avg_image_width: Average image width
        avg_image_height: Average image height
        detail: Image detail level
        
    Returns:
        Dictionary with cost breakdown
    """
    single_cost = calculate_single_extraction_cost(
        avg_image_width, avg_image_height, detail=detail
    )
    
    monthly_cost = single_cost["total_cost"] * extractions_per_month
    annual_cost = monthly_cost * 12
    
    return {
        "cost_per_extraction": single_cost["total_cost"],
        "monthly_cost": monthly_cost,
        "annual_cost": annual_cost,
        "extractions_per_month": extractions_per_month,
    }


def print_cost_breakdown(cost_data: Dict[str, float], title: str = "Cost Breakdown"):
    """Print formatted cost breakdown."""
    print(f"\n{title}")
    print("=" * 60)
    print(f"Text Input Tokens:     {cost_data['text_input_tokens']:,}")
    print(f"Image Input Tokens:    {cost_data['image_input_tokens']:,}")
    print(f"Total Input Tokens:    {cost_data['total_input_tokens']:,}")
    print(f"Output Tokens:         {cost_data['output_tokens']:,}")
    print("-" * 60)
    print(f"Input Cost:            ${cost_data['input_cost']:.6f}")
    print(f"Output Cost:           ${cost_data['output_cost']:.6f}")
    print(f"Total Cost:            ${cost_data['total_cost']:.6f}")
    print("=" * 60)


def print_monthly_summary(monthly_data: Dict[str, float]):
    """Print monthly cost summary."""
    print(f"\nMonthly Cost Summary")
    print("=" * 60)
    print(f"Extractions/Month:     {monthly_data['extractions_per_month']:,}")
    print(f"Cost per Extraction:   ${monthly_data['cost_per_extraction']:.6f}")
    print(f"Monthly Cost:          ${monthly_data['monthly_cost']:.2f}")
    print(f"Annual Cost:           ${monthly_data['annual_cost']:.2f}")
    print("=" * 60)


def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Calculate API costs for token extraction"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Image width in pixels (default: 1920)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Image height in pixels (default: 1080)"
    )
    parser.add_argument(
        "--output-tokens",
        type=int,
        default=None,
        help="Number of output tokens (default: 1000)"
    )
    parser.add_argument(
        "--detail",
        choices=["high", "low"],
        default="high",
        help="Image detail level (default: high)"
    )
    parser.add_argument(
        "--monthly",
        type=int,
        default=None,
        help="Calculate monthly cost for N extractions"
    )
    parser.add_argument(
        "--scenarios",
        action="store_true",
        help="Show common usage scenarios"
    )
    
    args = parser.parse_args()
    
    if args.scenarios:
        print("\n" + "=" * 60)
        print("Common Usage Scenarios")
        print("=" * 60)
        
        scenarios = [
            ("Small (1280x720)", 1280, 1080),
            ("Standard (1920x1080)", 1920, 1080),
            ("Large (2000x1200)", 2000, 1200),
        ]
        
        for name, width, height in scenarios:
            cost = calculate_single_extraction_cost(width, height, detail=args.detail)
            print(f"\n{name}:")
            print(f"  Cost per extraction: ${cost['total_cost']:.6f}")
            if args.monthly:
                monthly = calculate_monthly_cost(args.monthly, width, height, args.detail)
                print(f"  Monthly ({args.monthly:,} extractions): ${monthly['monthly_cost']:.2f}")
        
        print("\n" + "=" * 60)
        print("Monthly Projections (Standard 1920x1080 images)")
        print("=" * 60)
        
        monthly_scenarios = [100, 1000, 10000, 100000]
        for count in monthly_scenarios:
            monthly = calculate_monthly_cost(count, 1920, 1080, args.detail)
            print(f"{count:>7,} extractions/month: ${monthly['monthly_cost']:>10,.2f}/mo (${monthly['annual_cost']:>10,.2f}/yr)")
        
        return
    
    # Single extraction cost
    cost_data = calculate_single_extraction_cost(
        args.width,
        args.height,
        args.output_tokens,
        args.detail
    )
    
    print_cost_breakdown(cost_data, f"Single Extraction Cost ({args.width}x{args.height})")
    
    if args.monthly:
        monthly_data = calculate_monthly_cost(
            args.monthly,
            args.width,
            args.height,
            args.detail
        )
        print_monthly_summary(monthly_data)


if __name__ == "__main__":
    main()

