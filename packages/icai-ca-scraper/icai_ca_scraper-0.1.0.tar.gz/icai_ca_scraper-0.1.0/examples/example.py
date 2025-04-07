from ca_scraper import CAScraper
import json

def main():
    # Initialize the scraper with a 1-second delay between requests
    scraper = CAScraper(delay_between_requests=1.0)
    
    # Example: Get details for a single member
    member_no = 100000
    details = scraper.get_member_details(member_no)
    if details:
        print(f"Found details for member {member_no}:")
        print(json.dumps(details, indent=2))
    else:
        print(f"No details found for member {member_no}")
    
    # Example: Get details for multiple members
    member_numbers = [100001, 100002, 100003, 100004, 100005]
    print(f"\nFetching details for {len(member_numbers)} members...")
    
    results = scraper.get_multiple_members(member_numbers)
    
    # Save results to file
    output_file = "ca_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nFound details for {len(results)} members")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main() 