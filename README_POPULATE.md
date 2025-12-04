# Populating Elasticsearch with Christmas Gift Data

This guide explains how to populate your Elasticsearch instance with the 12 Days of Christmas dataset.

## Overview

The `populate_elasticsearch.py` script creates **78 documents** in total:
- Day 1: 1 document about "a Partridge in a Pear Tree"
- Day 2: 2 documents about "Turtle Doves"
- Day 3: 3 documents about "French Hens"
- ...continuing through...
- Day 12: 12 documents about "Drummers Drumming"

## Prerequisites

1. An Elasticsearch instance (Elasticsearch 8.0+)
2. An API key with permissions to create indices and index documents
3. Python dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your Elasticsearch credentials:
   ```bash
   ES_ENDPOINT=https://your-project.es.region.azure.elastic.cloud:443
   ES_API_KEY=your-api-key-here
   ES_INDEX_NAME=christmas-gifts
   ```

## Usage

### First Time Setup (Create Index and Populate)

```bash
python populate_elasticsearch.py
```

This will:
1. Connect to your Elasticsearch instance
2. Create the `christmas-gifts` index (if it doesn't exist)
3. Generate 78 unique documents
4. Bulk index all documents
5. Verify the counts are correct

### Delete and Recreate

If you need to start fresh:

```bash
python populate_elasticsearch.py --delete
```

### Verify Counts Only

To check if your index has the correct number of documents:

```bash
python populate_elasticsearch.py --verify
```

## Expected Output

When successful, you should see:

```
🔍 Verifying Document Counts
============================================================
✅ Day  1:  1/ 1 documents - a Partridge in a Pear Tree
✅ Day  2:  2/ 2 documents - Turtle Doves
✅ Day  3:  3/ 3 documents - French Hens
✅ Day  4:  4/ 4 documents - Calling Birds
✅ Day  5:  5/ 5 documents - Golden Rings
✅ Day  6:  6/ 6 documents - Geese a-Laying
✅ Day  7:  7/ 7 documents - Swans a-Swimming
✅ Day  8:  8/ 8 documents - Maids a-Milking
✅ Day  9:  9/ 9 documents - Ladies Dancing
✅ Day 10: 10/10 documents - Lords a-Leaping
✅ Day 11: 11/11 documents - Pipers Piping
✅ Day 12: 12/12 documents - Drummers Drumming
============================================================
📊 Total documents: 78/78
🎉 All document counts are correct!
```

## Document Structure

Each document contains:

```json
{
  "title": "Golden Rings - Document 1",
  "content": "Golden rings are perhaps the most iconic gift...",
  "gift_name": "Golden Rings",
  "day": 5,
  "doc_number": 1
}
```

## Next Steps

After populating Elasticsearch:

1. **Configure Elastic Agent Builder**:
   - Create an ES|QL tool to search the `christmas-gifts` index
   - Set up the agent to query based on gift names or day numbers

2. **Test the Integration**:
   ```bash
   # Search for all gifts
   python main.py --elastic
   
   # Search for a specific day
   python main.py --elastic --day 5
   ```

## Troubleshooting

### Connection Errors

If you see connection errors:
- Verify your `ES_ENDPOINT` is correct and includes the port (`:443`)
- Ensure your `ES_API_KEY` has the necessary permissions
- Check that your Elasticsearch instance is running and accessible

### Wrong Document Counts

If the verification shows incorrect counts:
- Run with `--delete` to recreate the index from scratch
- Check Elasticsearch logs for indexing errors

### Import Errors

If you get import errors for `elasticsearch`:
```bash
pip install -r requirements.txt
```

## Content Quality

Each gift has unique, educational content:
- Multiple variations to ensure each document is distinct
- Historical and symbolic information about each gift
- References to religious symbolism (for educational purposes)
- Cultural context about the Christmas tradition

This ensures that when the Elastic Agent Builder searches for documents, it finds meaningful, varied content that helps demonstrate the power of semantic search.
