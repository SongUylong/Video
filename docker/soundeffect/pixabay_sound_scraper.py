#!/usr/bin/env python3
"""
Pixabay Sound Effects Scraper (Selenium Version)
Downloads swoosh sound effects from Pixabay using Selenium for browser emulation
"""

import os
import re
import time
import requests
from pathlib import Path
from urllib.parse import urljoin

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Warning: Selenium not available. Install with: conda install -y selenium geckodriver -c conda-forge")


class PixabaySoundScraper:
    def __init__(self, output_dir="sound_effects", use_selenium=True):
        self.base_url = "https://pixabay.com"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        
        # Headers for requests fallback
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Setup Selenium driver
        self.driver = None
        if self.use_selenium:
            self._setup_selenium()
    
    def _setup_selenium(self):
        """Setup Selenium WebDriver with Chrome"""
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            print("✓ Selenium WebDriver initialized")
        except Exception as e:
            print(f"Warning: Could not initialize Selenium: {e}")
            self.use_selenium = False
            self.driver = None
    
    
    def get_search_results(self, search_term="swoosh", page=1):
        """Get sound effects from search results page"""
        url = f"{self.base_url}/sound-effects/search/{search_term}/"
        if page > 1:
            url += f"?pagi={page}"
        
        print(f"Fetching search results from: {url}")
        
        if self.use_selenium and self.driver:
            return self._get_results_selenium(url)
        else:
            print("Selenium not available, trying direct API method...")
            return self._get_results_api(search_term, page)
    
    def _get_results_selenium(self, url):
        """Get results using Selenium"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Find all sound effect rows
            sound_rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.audioRow--nAm4Z')
            
            results = []
            for row in sound_rows[:20]:  # Limit to first 20
                try:
                    # Get title and URL
                    title_elem = row.find_element(By.CSS_SELECTOR, 'a.title--7N7Nr')
                    title = title_elem.text.strip()
                    detail_url = title_elem.get_attribute('href')
                    
                    # Get author
                    try:
                        author_elem = row.find_element(By.CSS_SELECTOR, 'a.name--yfZpi')
                        author = author_elem.text.strip()
                    except:
                        author = "Unknown"
                    
                    # Try to get download button
                    download_url = None
                    try:
                        download_btn = row.find_element(By.CSS_SELECTOR, 'button[aria-label="Download"]')
                        # Click might trigger download modal, we'll handle in detail page
                    except:
                        pass
                    
                    results.append({
                        'title': title,
                        'author': author,
                        'url': detail_url,
                        'download_url': download_url
                    })
                    
                except Exception as e:
                    print(f"Error parsing sound row: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"Selenium error: {e}")
            return []
    
    def _get_results_api(self, search_term, page):
        """Fallback method using Pixabay API if available"""
        # Note: This requires Pixabay API key
        # For now, return empty - user would need to get API key
        print("API method not implemented. Please install Selenium.")
        print("Run: conda install -y selenium python-chromedriver-binary -c conda-forge")
        return []
    
    
    def get_download_url(self, detail_url):
        """Extract the actual download URL from a sound effect detail page"""
        print(f"Getting download URL from: {detail_url}")
        
        if self.use_selenium and self.driver:
            return self._get_download_url_selenium(detail_url)
        else:
            return None
    
    def _get_download_url_selenium(self, detail_url):
        """Get download URL using Selenium"""
        try:
            self.driver.get(detail_url)
            time.sleep(2)
            
            # Try to find the download link
            # Method 1: Look for the main download button and extract href
            try:
                download_btn = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[download], button[aria-label="Download"]'))
                )
                
                # If it's an anchor tag, get href directly
                if download_btn.tag_name == 'a':
                    download_url = download_btn.get_attribute('href')
                    if download_url and '.mp3' in download_url:
                        return download_url
                
                # If it's a button, click it and look for the actual download link
                download_btn.click()
                time.sleep(1)
                
                # Look for the generated download link
                links = self.driver.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    if href and '.mp3' in href and 'download' in href.lower():
                        return href
                        
            except Exception as e:
                print(f"Method 1 failed: {e}")
            
            # Method 2: Look for audio source in the page
            try:
                audio_elem = self.driver.find_element(By.TAG_NAME, 'audio')
                source_elem = audio_elem.find_element(By.TAG_NAME, 'source')
                src = source_elem.get_attribute('src')
                if src and '.mp3' in src:
                    return src
            except Exception as e:
                print(f"Method 2 failed: {e}")
            
            # Method 3: Check page source for MP3 URLs
            try:
                page_source = self.driver.page_source
                mp3_matches = re.findall(r'https://[^\s"\'<>]+\.mp3', page_source)
                if mp3_matches:
                    # Filter for valid download URLs
                    for url in mp3_matches:
                        if 'cdn.pixabay.com' in url or 'download' in url.lower():
                            return url
            except Exception as e:
                print(f"Method 3 failed: {e}")
            
            print(f"Could not find download link for {detail_url}")
            return None
            
        except Exception as e:
            print(f"Error getting download URL: {e}")
            return None
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("✓ Browser driver closed")
            except:
                pass
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def download_sound(self, url, filename):
        """Download a sound effect file"""
        filepath = self.output_dir / filename
        
        # Skip if already exists
        if filepath.exists():
            print(f"File already exists: {filename}")
            return True
        
        try:
            print(f"Downloading: {filename}")
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            # Write to file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✓ Downloaded: {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Error downloading {filename}: {e}")
            return False
    
    def scrape_and_download(self, search_term="swoosh", max_pages=1, max_sounds=20):
        """Main method to scrape and download sound effects"""
        print(f"Starting scrape for '{search_term}'")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("-" * 60)
        
        downloaded = 0
        total_found = 0
        
        try:
            for page in range(1, max_pages + 1):
                if downloaded >= max_sounds:
                    break
                
                print(f"\nPage {page}:")
                results = self.get_search_results(search_term, page)
                total_found += len(results)
                
                print(f"Found {len(results)} sound effects on page {page}")
                
                for sound in results:
                    if downloaded >= max_sounds:
                        break
                    
                    print(f"\n[{downloaded + 1}/{max_sounds}] {sound['title']} by {sound['author']}")
                    
                    # Get download URL
                    download_url = self.get_download_url(sound['url'])
                    
                    if download_url:
                        # Create filename
                        safe_title = self.sanitize_filename(sound['title'])
                        safe_author = self.sanitize_filename(sound['author'])
                        filename = f"{safe_title}_{safe_author}.mp3"
                        
                        # Download
                        if self.download_sound(download_url, filename):
                            downloaded += 1
                    
                    # Be nice to the server
                    time.sleep(2)
        
        finally:
            # Always cleanup
            self.cleanup()
        
        print("\n" + "=" * 60)
        print(f"Scraping complete!")
        print(f"Found: {total_found} sound effects")
        print(f"Downloaded: {downloaded} files")
        print(f"Location: {self.output_dir.absolute()}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download sound effects from Pixabay')
    parser.add_argument('search', nargs='?', default='swoosh', help='Search term (default: swoosh)')
    parser.add_argument('-o', '--output', default='sound_effects', help='Output directory')
    parser.add_argument('-n', '--number', type=int, default=20, help='Max number of sounds to download')
    parser.add_argument('-p', '--pages', type=int, default=2, help='Max number of pages to scrape')
    
    args = parser.parse_args()
    
    scraper = PixabaySoundScraper(output_dir=args.output)
    scraper.scrape_and_download(
        search_term=args.search,
        max_pages=args.pages,
        max_sounds=args.number
    )


if __name__ == "__main__":
    main()
