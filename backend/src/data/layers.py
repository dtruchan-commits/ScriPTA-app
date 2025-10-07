from ..models.models import LayerColor, LayerConfig, LayerConfigSet, LayerName

LAYER_DATA = [
    LayerConfigSet(
        config_name="default",
        layers=[
            LayerConfig(name=LayerName.DIELINE, locked=True, print=True, color=LayerColor.GOLD),
            LayerConfig(name=LayerName.TECHNICAL, locked=True, print=True, color=LayerColor.TEAL),
            LayerConfig(name=LayerName.BRAILLE_EMB, locked=True, print=True, color=LayerColor.FIESTA),
            LayerConfig(name=LayerName.TEXT, locked=False, print=True, color=LayerColor.LIGHT_BLUE),
            LayerConfig(name=LayerName.ACF_HRL, locked=False, print=True, color=LayerColor.YELLOW),
            LayerConfig(name=LayerName.ACF_LRA_VARNISH, locked=False, print=True, color=LayerColor.GREEN),
            LayerConfig(name=LayerName.DESIGN, locked=False, print=True, color=LayerColor.RED),
            LayerConfig(name=LayerName.INFOBOX, locked=True, print=True, color=LayerColor.LAVENDER),
            LayerConfig(name=LayerName.GUIDES, locked=True, print=False, color=LayerColor.GRAY),
        ]
    ),
    LayerConfigSet(
        config_name="FoldingBox",
        layers=[
            LayerConfig(name=LayerName.DIELINE, locked=True, print=True, color=LayerColor.GOLD),
            LayerConfig(name=LayerName.TECHNICAL, locked=True, print=True, color=LayerColor.TEAL),
            LayerConfig(name=LayerName.BRAILLE_EMB, locked=True, print=True, color=LayerColor.FIESTA),
            LayerConfig(name=LayerName.TEXT, locked=False, print=True, color=LayerColor.LIGHT_BLUE),
            LayerConfig(name=LayerName.ACF_HRL, locked=False, print=True, color=LayerColor.YELLOW),
            LayerConfig(name=LayerName.ACF_LRA_VARNISH, locked=False, print=True, color=LayerColor.GREEN),
            LayerConfig(name=LayerName.DESIGN, locked=False, print=True, color=LayerColor.RED),
            LayerConfig(name=LayerName.INFOBOX, locked=True, print=True, color=LayerColor.LAVENDER),
            LayerConfig(name=LayerName.GUIDES, locked=True, print=False, color=LayerColor.GRAY),
        ]
    ),
    LayerConfigSet(
        config_name="Label",
        layers=[
            LayerConfig(name=LayerName.TEXT, locked=False, print=True, color=LayerColor.LIGHT_BLUE),
            LayerConfig(name=LayerName.DESIGN, locked=False, print=True, color=LayerColor.RED),
            LayerConfig(name=LayerName.GUIDES, locked=True, print=False, color=LayerColor.GRAY),
            LayerConfig(name=LayerName.DIELINE, locked=True, print=True, color=LayerColor.GOLD),
        ]
    ),
    LayerConfigSet(
        config_name="TPM",
        layers=[
            LayerConfig(name=LayerName.GUIDES, locked=False, print=True, color=LayerColor.GRAY),
            LayerConfig(name=LayerName.PANEL, locked=False, print=True, color=LayerColor.BLUE),
            LayerConfig(name=LayerName.DIELINE, locked=False, print=True, color=LayerColor.GOLD),
        ]
    ),
]
