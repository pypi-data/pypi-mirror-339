import setuptools

setuptools.setup(
    name="odoo_addon_community_maps",
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        "external_dependencies_override": {
            "python": {
                "python-slugify": "python-slugify==8.0.1",
            },
        },
    },
)
