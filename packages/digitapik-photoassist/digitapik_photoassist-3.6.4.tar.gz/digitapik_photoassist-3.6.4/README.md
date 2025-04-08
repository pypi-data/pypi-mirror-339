# digitapik_photoassist  
**AI-powered photo analysis and categorization**  

## Overview  
`digitapik_photoassist` is a powerful Python package that leverages AI to analyze, categorize, and enhance images with precision. Whether you're an individual, business, or developer, this tool helps automate image processing with advanced machine learning capabilities provided by our powerful API.  

## Features  
[x] **AI-Powered Image Analysis** - Extract insights from images with deep learning.  
[x] **Automated Categorization** - Classify images into relevant categories.  
[x] **Metadata Extraction** - Retrieve EXIF data, colors, and other attributes.  
[x] **Face & Object Detection** - Identify faces, objects, and scenes in photos.  
[x] **Image Quality Assessment** - Score images based on clarity and noise levels.  

## Installation  
Install the package via pip:  
```bash
pip install digitapik-photoassist
```

## Usage  

### Importing the Package  
```python
from digitapik_photoassist import PhotoAssist
```

### Analyzing an Image  
```python
analyzer = PhotoAssist()
result = analyzer.analyze("image.jpg")
print(result)
```

### Categorizing Images  
```python
category = analyzer.categorize("image.jpg")
print(f"Category: {category}")
```

### Extracting Metadata  
```python
metadata = analyzer.get_metadata("image.jpg")
print(metadata)
```

### Face and Object Detection  
```python
detections = analyzer.detect_objects("image.jpg")
print(detections)
```

### Enhancing Image Quality  
```python
enhanced_image = analyzer.enhance("image.jpg")
enhanced_image.save("enhanced_image.jpg")
```

## Licensing  

`digitapik_photoassist` is **dual-licensed** under:  

- **MIT License** (Open-Source Version) - Free for non-commercial, educational, and personal use.  
- **Commercial License** - Required for business or enterprise use.  

### Commercial License  
If you are using this package in a **commercial product, SaaS, or enterprise application**, you must obtain a **commercial license**.  

**For licensing inquiries, please contact:** `support@digitapik.com`  

## Roadmap  
**Upcoming Features**  
- Advanced OCR for text extraction  
- Support for cloud-based processing  
- Batch image processing  

## Contributing  
Contributions are welcome! Feel free to submit a pull request or open an issue.  

## License  
This project is available under the **MIT License** for non-commercial use.  
For commercial use, please obtain a license. 