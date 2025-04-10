class Event:
    def __init__(self, channel: str, data: str) -> None:
        self.channel = channel
        self.data = data

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Event)
            and self.channel == other.channel
            and self.data == other.data
        )
    

    def __repr__(self) -> str:
        # Limit data representation length for cleaner logs
        data_repr = repr(self.data)
        if len(data_repr) > 100:
            data_repr = data_repr[:100] + '...'
        return f"Event(channel={self.channel!r}, data={data_repr})"

