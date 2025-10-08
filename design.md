# Design Document

## Overview

The Instagram Image Downloader Bot is a Python-based application that automates the process of downloading images from Instagram. The system uses web scraping techniques combined with Instagram's public APIs where available. The architecture follows a modular design with separate components for authentication, content extraction, download management, and user interface.

## Architecture

The system follows a layered architecture pattern:

```
┌─────────────────────────────────────┐
│           User Interface            │
│        (CLI/GUI Interface)          │
├─────────────────────────────────────┤
│         Service Layer               │
│  (Download Manager, Progress)       │
├─────────────────────────────────────┤
│        Business Logic              │
│ (Content Extractor, URL Parser)    │
├─────────────────────────────────────┤
│         Data Access Layer          │
│   (HTTP Client, File Manager)      │
├─────────────────────────────────────┤
│        External Services           │
│      (Instagram Platform)          │
└─────────────────────────────────────┘
```

## Components and Interfaces

### 1. URL Parser Component
- **Purpose**: Parse and validate Instagram URLs
- **Interface**: 
  - `parse_url(url: str) -> URLInfo`
  - `validate_url(url: str) -> bool`
- **Responsibilities**: Extract content type (post, story, profile), username, and content ID

### 2. Authentication Manager
- **Purpose**: Handle Instagram login and session management
- **Interface**:
  - `authenticate(username: str, password: str) -> Session`
  - `is_authenticated() -> bool`
  - `refresh_session() -> bool`
- **Responsibilities**: Manage login credentials, maintain session cookies, handle 2FA if required

### 3. Content Extractor
- **Purpose**: Extract image URLs and metadata from Instagram pages
- **Interface**:
  - `extract_post_images(post_url: str) -> List[ImageInfo]`
  - `extract_story_images(username: str) -> List[ImageInfo]`
  - `extract_profile_images(username: str) -> List[ImageInfo]`
- **Responsibilities**: Parse HTML/JSON responses, extract image URLs, gather metadata

### 4. Download Manager
- **Purpose**: Handle the actual downloading of images with rate limiting
- **Interface**:
  - `download_image(image_info: ImageInfo, destination: str) -> bool`
  - `download_batch(images: List[ImageInfo], destination: str) -> DownloadResult`
- **Responsibilities**: Download files, implement rate limiting, handle retries, manage concurrent downloads

### 5. Rate Limiter
- **Purpose**: Prevent being blocked by implementing intelligent delays
- **Interface**:
  - `can_make_request() -> bool`
  - `record_request()`
  - `get_delay() -> float`
- **Responsibilities**: Track request frequency, implement exponential backoff, randomize delays

### 6. File Manager
- **Purpose**: Handle file operations and organization
- **Interface**:
  - `create_filename(image_info: ImageInfo) -> str`
  - `ensure_directory(path: str) -> bool`
  - `save_image(image_data: bytes, filepath: str) -> bool`
- **Responsibilities**: Generate descriptive filenames, create directories, handle file conflicts

### 7. Progress Reporter
- **Purpose**: Provide user feedback on download progress
- **Interface**:
  - `start_progress(total_items: int)`
  - `update_progress(completed: int, current_item: str)`
  - `finish_progress(summary: DownloadSummary)`
- **Responsibilities**: Display progress bars, show current status, report completion statistics

## Data Models

### URLInfo
```python
@dataclass
class URLInfo:
    content_type: str  # 'post', 'story', 'profile'
    username: str
    content_id: Optional[str]
    is_valid: bool
```

### ImageInfo
```python
@dataclass
class ImageInfo:
    url: str
    filename: str
    username: str
    post_id: Optional[str]
    caption: Optional[str]
    timestamp: datetime
    file_size: Optional[int]
```

### DownloadResult
```python
@dataclass
class DownloadResult:
    successful_downloads: int
    failed_downloads: int
    total_size: int
    errors: List[str]
    duration: float
```

### Session
```python
@dataclass
class Session:
    cookies: Dict[str, str]
    headers: Dict[str, str]
    csrf_token: str
    user_id: str
    is_authenticated: bool
```

## Error Handling

### Error Categories
1. **Network Errors**: Connection timeouts, DNS failures
2. **Authentication Errors**: Invalid credentials, 2FA required, account locked
3. **Rate Limiting**: Too many requests, temporary blocks
4. **Content Errors**: Private profiles, deleted content, invalid URLs
5. **File System Errors**: Permission denied, disk full, invalid paths

### Error Handling Strategy
- **Retry Logic**: Implement exponential backoff for transient errors
- **Graceful Degradation**: Continue with available content when some items fail
- **User Notification**: Provide clear, actionable error messages
- **Logging**: Detailed logging for debugging and monitoring

### Rate Limiting Response
```python
class RateLimitHandler:
    def handle_rate_limit(self, response_code: int) -> int:
        if response_code == 429:
            return self.exponential_backoff()
        elif response_code == 403:
            return self.long_delay()
        return 0
```

## Testing Strategy

### Unit Testing
- **URL Parser**: Test various Instagram URL formats
- **Content Extractor**: Mock Instagram responses, test parsing logic
- **Rate Limiter**: Test delay calculations and request tracking
- **File Manager**: Test filename generation and file operations

### Integration Testing
- **Authentication Flow**: Test login process with test accounts
- **Download Pipeline**: End-to-end testing with sample content
- **Error Scenarios**: Test handling of various error conditions

### Test Data Management
- Use Instagram test accounts for authentication testing
- Create mock responses for content extraction testing
- Test with various content types (posts, stories, profiles)

### Performance Testing
- **Rate Limiting**: Verify delays are working correctly
- **Concurrent Downloads**: Test multiple simultaneous downloads
- **Memory Usage**: Monitor memory consumption with large batches

## Security Considerations

### Credential Management
- Store credentials securely (encrypted or in secure storage)
- Support environment variables for automation
- Clear sensitive data from memory after use

### Request Headers
- Use realistic User-Agent strings
- Rotate headers to avoid detection
- Include appropriate referrer headers

### Legal Compliance
- Respect robots.txt and terms of service
- Only download publicly accessible content
- Implement opt-out mechanisms for content creators

## Implementation Notes

### Technology Stack
- **Language**: Python 3.8+
- **HTTP Client**: requests or httpx for async support
- **HTML Parsing**: BeautifulSoup4 or lxml
- **JSON Handling**: Built-in json module
- **CLI Interface**: Click or argparse
- **Progress Display**: tqdm or rich

### External Dependencies
- Instagram's web interface (no official API for image downloading)
- Potential use of instagram-private-api for authenticated requests
- File system for local storage

### Deployment Considerations
- Package as standalone executable using PyInstaller
- Support for configuration files
- Cross-platform compatibility (Windows, macOS, Linux)