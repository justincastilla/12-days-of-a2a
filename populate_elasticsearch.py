#!/usr/bin/env python3
"""
Populate Elasticsearch with 12 Days of Christmas Documents

This script creates an Elasticsearch index and populates it with documents
for each gift from the "12 Days of Christmas" song. The number of documents
for each day matches the day number (1 doc for day 1, 2 for day 2, etc.).

Usage:
    python populate_elasticsearch.py              # Create index and populate
    python populate_elasticsearch.py --delete     # Delete and recreate index
    python populate_elasticsearch.py --verify     # Verify document counts
"""

import argparse
import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

# Load environment variables
load_dotenv()

# Elasticsearch configuration
ES_ENDPOINT = os.getenv("ES_ENDPOINT")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX_NAME = os.getenv("ES_INDEX_NAME", "christmas-gifts")

# Gift data matching the structure in gift_agents.py
GIFTS = {
    1: {"gift": "a Partridge in a Pear Tree", "quantity": 1},
    2: {"gift": "Turtle Doves", "quantity": 2},
    3: {"gift": "French Hens", "quantity": 3},
    4: {"gift": "Calling Birds", "quantity": 4},
    5: {"gift": "Golden Rings", "quantity": 5},
    6: {"gift": "Geese a-Laying", "quantity": 6},
    7: {"gift": "Swans a-Swimming", "quantity": 7},
    8: {"gift": "Maids a-Milking", "quantity": 8},
    9: {"gift": "Ladies Dancing", "quantity": 9},
    10: {"gift": "Lords a-Leaping", "quantity": 10},
    11: {"gift": "Pipers Piping", "quantity": 11},
    12: {"gift": "Drummers Drumming", "quantity": 12},
}

# Content variations for each gift to create unique documents
GIFT_CONTENT = {
    1: [
        "The partridge is a medium-sized game bird native to Europe and Asia. In the famous Christmas carol, it sits majestically in a pear tree, symbolizing the first day of Christmas and representing Jesus Christ in religious interpretations.",
    ],
    2: [
        "Turtle doves are symbols of devoted love and peace. These gentle birds mate for life, making them perfect representatives of enduring affection in the Christmas carol.",
        "The turtle dove, despite its name, is not related to sea turtles but is actually a member of the dove family. Their soft cooing and loyal nature have made them symbols of romance throughout history.",
    ],
    3: [
        "French hens, also known as Faverolles or other French chicken breeds, were once considered luxury poultry. These prized birds represented wealth and prosperity during the Christmas season.",
        "The three French hens in the carol symbolize faith, hope, and charity - the three theological virtues. These beautiful birds were highly valued in medieval times for their meat and eggs.",
        "French chickens were imported to England as exotic, high-quality poultry. Their presence in the Christmas carol reflects the giving of valuable, premium gifts during the holiday season.",
    ],
    4: [
        "Calling birds, sometimes interpreted as 'colly birds' (meaning coal-black birds), are often thought to be blackbirds. Their melodious songs fill the winter air with beautiful music.",
        "The four calling birds represent the four Gospels of the New Testament: Matthew, Mark, Luke, and John, who spread the good news through their writings.",
        "These songbirds were prized for their beautiful voices. In medieval times, keeping singing birds was a sign of refinement and culture among the nobility.",
        "Calling birds, with their cheerful songs, symbolize the spreading of joyful news during the Christmas season. Their voices unite to create a harmonious celebration.",
    ],
    5: [
        "Golden rings are perhaps the most iconic gift in the Twelve Days of Christmas. These precious circles of gold symbolize eternal love, commitment, and the unending circle of life.",
        "The five golden rings represent the first five books of the Old Testament: Genesis, Exodus, Leviticus, Numbers, and Deuteronomy, known as the Pentateuch or Torah.",
        "Gold rings were among the most valuable gifts one could give, representing wealth, status, and deep affection. Their brilliance and durability made them perfect symbols of lasting love.",
        "These golden bands, shining brightly in the winter light, represent the precious nature of the Christmas gift-giving tradition and the value of cherished relationships.",
        "Five golden rings, each one a perfect circle, symbolize completeness and perfection. Their golden glow brings warmth and light to the cold winter season.",
    ],
    6: [
        "Geese a-laying provide both eggs and meat, making them valuable farm animals. A laying goose represents productivity and the abundance of the harvest season.",
        "The six geese a-laying symbolize the six days of creation in the biblical account, representing God's creative power and the gift of the natural world.",
        "Geese were important domesticated birds in medieval England, prized for their eggs, meat, feathers, and down. A laying goose was a gift that kept on giving.",
        "These productive birds represent fertility and abundance. Their eggs were valuable sources of nutrition, especially during the winter months when food was scarce.",
        "Geese have been domesticated for thousands of years. Their distinctive honking and communal nature make them memorable residents of farms and estates.",
        "Six geese a-laying represents the ongoing cycle of life and productivity, a perfect gift for sustaining a household through the long winter season.",
    ],
    7: [
        "Swans are elegant waterfowl known for their grace and beauty. Seven swans a-swimming glide majestically across lakes and ponds, embodying natural elegance.",
        "The seven swans represent the seven gifts of the Holy Spirit: wisdom, understanding, counsel, fortitude, knowledge, piety, and fear of the Lord.",
        "Swans mate for life and are symbols of loyalty, grace, and transformation. Their white plumage and curved necks create one of nature's most beautiful silhouettes.",
        "These majestic birds were royal property in England, with most swans belonging to the Crown. Giving swans was a gift of extraordinary value and prestige.",
        "Seven swans swimming in formation create a breathtaking sight. Their synchronized movements and elegant presence make them natural symbols of harmony and beauty.",
        "The swan's transformation from an awkward cygnet to a graceful adult mirrors the theme of transformation and renewal central to the Christmas season.",
        "Swans have been featured in mythology and folklore for centuries, often representing purity, grace, and the soul's journey toward enlightenment.",
    ],
    8: [
        "Maids a-milking represent the essential agricultural work of dairy farming. Eight maidens working together show the value of community labor and cooperation.",
        "The eight maids a-milking symbolize the eight Beatitudes from Jesus's Sermon on the Mount, representing the path to spiritual blessing and righteousness.",
        "Milkmaids were vital workers on farms and estates, rising early each morning to milk the cows and ensure fresh dairy products for the household.",
        "Eight maids working together could process milk from entire herds, producing butter, cheese, and cream - valuable commodities in the pre-industrial economy.",
        "The rhythmic work of milking was often accompanied by songs and conversation, making the milkmaids symbols of cheerful labor and rural community.",
        "Fresh milk and dairy products were essential parts of the winter diet, and skilled milkmaids were highly valued members of any agricultural estate.",
        "These hardworking women represented the backbone of rural food production, transforming the farm's resources into valuable, nutritious products.",
        "Eight maids a-milking shows the multiplication of labor and productivity, with many hands making light work of the daily dairy tasks.",
    ],
    9: [
        "Ladies dancing bring joy and celebration to any gathering. Nine noble ladies performing elegant dances represent festivity, culture, and social refinement.",
        "The nine ladies dancing symbolize the nine fruits of the Holy Spirit: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control.",
        "Court dances in medieval times were elaborate affairs requiring skill, grace, and extensive practice. Dancing ladies represented culture and sophistication.",
        "Nine ladies dancing in coordinated patterns create a spectacular display of human artistry and physical grace, perfect for celebrating the Christmas season.",
        "Dancing was an essential social skill among the nobility, and accomplished dancers brought entertainment and elegance to holiday celebrations.",
        "The gift of dancers represents the joy and merriment of the Christmas season, where music and movement combine to create celebration.",
        "These nine ladies, moving in harmony to festive music, embody the spirit of celebration and the importance of artistic expression during the holidays.",
        "Court dances often told stories or represented seasonal themes, making the dancers both entertainers and storytellers during Christmas festivities.",
        "Nine dancing ladies represent the multiplication of joy, as each dancer adds their unique grace to the collective celebration of the season.",
    ],
    10: [
        "Lords a-leaping display athletic prowess and noble bearing. Ten lords jumping high represent vitality, energy, and the exuberance of celebration.",
        "The ten lords a-leaping symbolize the Ten Commandments, the fundamental laws given to Moses that guide moral and ethical behavior.",
        "Leaping lords perform acrobatic feats and energetic dances, bringing dynamic movement and excitement to Christmas celebrations.",
        "In medieval entertainment, athletic displays by noblemen demonstrated their physical fitness, courage, and vitality - qualities befitting their station.",
        "Ten lords leaping in unison create a powerful spectacle of coordinated movement, showing the strength and energy of the Christmas season.",
        "These noble gentlemen, defying gravity with their leaps, represent the transcendent joy that lifts spirits during the darkest days of winter.",
        "Leaping dances were part of traditional celebrations, with lords demonstrating their agility and strength through impressive athletic movements.",
        "The ten lords represent authority and governance, while their leaping shows that even the powerful can experience childlike joy during Christmas.",
        "Each lord's leap represents aspiration and striving upward, symbolic of humanity's desire to reach toward higher ideals and spiritual growth.",
        "Ten lords a-leaping bring masculine energy and strength to balance the grace of the nine ladies dancing, creating perfect harmony in celebration.",
    ],
    11: [
        "Pipers piping fill the air with music, their bagpipes or flutes creating melodies that echo through halls and across fields during the Christmas season.",
        "The eleven pipers piping represent the eleven faithful Apostles (excluding Judas Iscariot), who spread the message of Christianity throughout the world.",
        "Pipers were essential musicians for celebrations, their instruments cutting through noise and distance to announce festivities and coordinate dancing.",
        "Eleven pipers playing in harmony create a rich tapestry of sound, with their different instruments blending to produce beautiful, complex music.",
        "The distinctive sound of pipes, whether bagpipes or other wind instruments, was central to medieval celebrations and could be heard from great distances.",
        "Pipers often led processions and called people to gather, making them symbols of community, announcement, and festive celebration.",
        "These eleven musicians represent the power of music to unite people, lift spirits, and create an atmosphere of joy during the Christmas season.",
        "Each piper contributes a unique voice to the ensemble, yet all must work in harmony to create the beautiful music of celebration.",
        "Pipers piping symbolize the call to worship, celebration, and community - bringing people together through the universal language of music.",
        "The eleven pipers, with their varied instruments and melodies, show how diversity in unity creates the most beautiful and complete celebrations.",
        "Traditional pipe music carries deep cultural significance, connecting present celebrations to ancient customs and the continuity of festive traditions.",
    ],
    12: [
        "Drummers drumming provide the rhythmic foundation for all celebration, their beats marking time and keeping dancers and musicians coordinated.",
        "The twelve drummers drumming represent the twelve points of doctrine in the Apostles' Creed, the fundamental statement of Christian belief.",
        "Drummers were essential to military and ceremonial functions, their powerful rhythms organizing large groups and announcing important occasions.",
        "Twelve drummers playing together create a thunderous, joyful noise that can be felt in the chest and heard across great distances.",
        "The drums' steady beat represents the heartbeat of celebration, the pulse that keeps all other music and movement in perfect time.",
        "Drummers symbolize strength, power, and the driving force that propels celebration forward with irresistible momentum.",
        "These twelve percussionists bring the Twelve Days of Christmas to a climactic conclusion with their powerful, commanding rhythms.",
        "Each drummer adds their own pattern to the collective rhythm, creating complex polyrhythms that showcase both individual skill and group coordination.",
        "The thunder of twelve drums represents the grand finale of the gift-giving, the culmination of the Christmas celebration with maximum fanfare.",
        "Drummers drumming connect earth and sky, their beats resonating through the ground while their sound rises to the heavens in celebration.",
        "The twelve drummers symbolize completion - the full cycle of the Twelve Days of Christmas, bringing the entire celebration to its joyful conclusion.",
        "With their drums, these twelve musicians announce that the Christmas season has reached its peak, calling all to join in the final celebration.",
    ],
}


def get_elasticsearch_client() -> Elasticsearch:
    """Create and return an Elasticsearch client."""
    if not ES_ENDPOINT or not ES_API_KEY:
        print("❌ Error: ES_ENDPOINT and ES_API_KEY must be set in .env file")
        sys.exit(1)

    print(f"🔗 Connecting to Elasticsearch at {ES_ENDPOINT}...")

    # Create client with API key authentication
    es = Elasticsearch(
        ES_ENDPOINT,
        api_key=ES_API_KEY,
        verify_certs=True,
    )

    # Test connection
    if not es.ping():
        print("❌ Error: Could not connect to Elasticsearch")
        sys.exit(1)

    print("✅ Successfully connected to Elasticsearch")
    return es


def create_index(es: Elasticsearch, delete_existing: bool = False):
    """Create the Elasticsearch index with proper mappings."""
    if es.indices.exists(index=ES_INDEX_NAME):
        if delete_existing:
            print(f"🗑️  Deleting existing index '{ES_INDEX_NAME}'...")
            es.indices.delete(index=ES_INDEX_NAME)
        else:
            print(
                f"ℹ️  Index '{ES_INDEX_NAME}' already exists (use --delete to recreate)"
            )
            return

    print(f"📝 Creating index '{ES_INDEX_NAME}'...")

    # Define index mappings
    mappings = {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "gift_name": {"type": "keyword"},
            "day": {"type": "integer"},
            "doc_number": {"type": "integer"},
        }
    }

    # Create index
    es.indices.create(index=ES_INDEX_NAME, mappings=mappings)
    print(f"✅ Index '{ES_INDEX_NAME}' created successfully")


def generate_documents() -> List[Dict]:
    """Generate all documents for the 12 days of Christmas."""
    documents = []

    for day in range(1, 13):
        gift_info = GIFTS[day]
        gift_name = gift_info["gift"]
        quantity = gift_info["quantity"]
        content_variations = GIFT_CONTENT[day]

        # Create the exact number of documents as the day number
        for doc_num in range(1, quantity + 1):
            # Use content variation, cycling if needed
            content = content_variations[(doc_num - 1) % len(content_variations)]

            doc = {
                "title": f"{gift_name} - Document {doc_num}",
                "content": content,
                "gift_name": gift_name,
                "day": day,
                "doc_number": doc_num,
            }
            documents.append(doc)

    return documents


def bulk_index_documents(es: Elasticsearch, documents: List[Dict]):
    """Bulk index all documents to Elasticsearch."""
    print(f"📤 Indexing {len(documents)} documents...")

    # Prepare bulk actions
    actions = [{"_index": ES_INDEX_NAME, "_source": doc} for doc in documents]

    # Perform bulk indexing
    success, failed = helpers.bulk(es, actions, raise_on_error=False, stats_only=True)

    print(f"✅ Successfully indexed {success} documents")
    if failed > 0:
        print(f"⚠️  Failed to index {failed} documents")

    # Refresh index to make documents immediately searchable
    es.indices.refresh(index=ES_INDEX_NAME)


def verify_counts(es: Elasticsearch):
    """Verify that document counts match expected values."""
    print("\n" + "=" * 60)
    print("🔍 Verifying Document Counts")
    print("=" * 60)

    all_correct = True
    total_docs = 0

    for day in range(1, 13):
        gift_info = GIFTS[day]
        expected_count = gift_info["quantity"]
        gift_name = gift_info["gift"]

        # Query for documents of this day
        result = es.count(index=ES_INDEX_NAME, query={"term": {"day": day}})
        actual_count = result["count"]
        total_docs += actual_count

        status = "✅" if actual_count == expected_count else "❌"
        print(
            f"{status} Day {day:2d}: {actual_count:2d}/{expected_count:2d} documents - {gift_name}"
        )

        if actual_count != expected_count:
            all_correct = False

    print("=" * 60)
    print(f"📊 Total documents: {total_docs}/78")

    if all_correct:
        print("🎉 All document counts are correct!")
    else:
        print("⚠️  Some document counts are incorrect")

    return all_correct


def main():
    """Main function to populate Elasticsearch."""
    parser = argparse.ArgumentParser(
        description="Populate Elasticsearch with 12 Days of Christmas documents"
    )
    parser.add_argument(
        "--delete", action="store_true", help="Delete and recreate the index"
    )
    parser.add_argument(
        "--verify", action="store_true", help="Only verify document counts"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🎄 12 Days of Christmas - Elasticsearch Populator")
    print("=" * 60)
    print()

    # Get Elasticsearch client
    es = get_elasticsearch_client()

    if args.verify:
        # Only verify counts
        verify_counts(es)
        return

    # Create index
    create_index(es, delete_existing=args.delete)

    # Generate documents
    print("\n📋 Generating documents...")
    documents = generate_documents()
    print(f"✅ Generated {len(documents)} documents (1+2+3+...+12 = 78)")

    # Index documents
    print()
    bulk_index_documents(es, documents)

    # Verify counts
    print()
    verify_counts(es)

    print("\n" + "=" * 60)
    print("🎉 Data population complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Configure your Elastic Agent Builder agent to search this index")
    print("2. Run: python main.py --elastic")
    print("3. Test specific days: python main.py --elastic --day 5")
    print()


if __name__ == "__main__":
    main()
