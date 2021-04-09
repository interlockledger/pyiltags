from io import BytesIO
from pyiltags.standard import ILStandardTagFactory, ILUInt64Tag

# Serialize a tag
tag = ILUInt64Tag(123456)
writer = BytesIO()
tag.serialize(writer)
writer.seek(0)
serialized = writer.read()
print(f'Tag with id {tag.id} and value {tag.value} serialized.')

# Unserialize the tag
reader = BytesIO(serialized)
factory = ILStandardTagFactory()
deserialized_tag = factory.deserialize(reader)
print(
    f'Deserialized tag with id {deserialized_tag.id} and value {deserialized_tag.value}.')
