"""Cognyx BOM SDK client."""

import asyncio

import httpx

from cognyx_bom_sdk.cognyx.helpers import format_bom, format_instance, get_parent_map
from cognyx_bom_sdk.cognyx.models import (
    BomEdge,
    BomNode,
    BomResponse,
    BomTree,
    GlobalSettingsResponse,
)


class CognyxClient:
    """Cognyx BOM SDK client."""

    def __init__(self, base_url: str, jwt_token: str) -> None:
        """Initialize the Cognyx client.

        Args:
            base_url: Base URL of the Cognyx API
            jwt_token: JWT token for authentication
        """
        self.base_url = base_url
        self.jwt_token = jwt_token

    async def get_bom(self, bom_id: str) -> BomResponse:
        """Get a BOM by ID.

        Args:
            bom_id: ID of the BOM to retrieve

        Returns:
            The BOM data
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/boms/{bom_id}",
                headers={"Authorization": f"Bearer {self.jwt_token}"},
            )
            response.raise_for_status()

            json = response.json()
            bom_data = json["data"]

            return BomResponse.model_validate(bom_data)

    async def get_default_view(self) -> str:
        """Get the default view for a BOM.

        Returns:
            The default view data
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/settings/global",
                headers={"Authorization": f"Bearer {self.jwt_token}"},
            )
            response.raise_for_status()

            settings = GlobalSettingsResponse.model_validate(response.json())

            return settings.features["projects"]["bom"]["default_view"]

    async def get_bom_tree(self, bom_id: str, view_id: str | None = None) -> BomTree:
        """Get a BOM as a tree.

        Args:
            bom_id: ID of the BOM
            view_id: ID of the view

        Returns:
            The BOM data as a tree
        """
        async with httpx.AsyncClient() as client:
            view_id = await self.get_default_view() if view_id is None else view_id

            response = await client.get(
                f"{self.base_url}/api/v1/boms/{bom_id}/tree",
                headers={"Authorization": f"Bearer {self.jwt_token}"},
                params={"view_id": view_id},
            )
            response.raise_for_status()

            return BomTree.model_validate(response.json())

    async def get_instance(
        self, instance_id: str, bom_id: str, view_id: str, parent_id: str | None = None
    ) -> dict:
        """Get a BOM instance by ID asynchronously.

        Args:
            instance_id: ID of the BOM instance to retrieve
            bom_id: ID of the BOM
            view_id: ID of the view
            parent_id: ID of the parent instance

        Returns:
            The BOM instance data
        """
        if parent_id is None:
            raise ValueError("Parent ID is required")
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/bom-instances/{instance_id}",
                headers={"Authorization": f"Bearer {self.jwt_token}"},
            )
            response.raise_for_status()
            json = response.json()

            return format_instance(json["data"], bom_id, view_id, parent_id)

    async def get_bom_instances(
        self,
        bom_id: str,
        nodes: list[BomNode],
        edges: list[BomEdge],
        view_id: str | None = None,
    ) -> list[dict]:
        """Get all BOM instances for a BOM.

        Args:
            bom_id: ID of the BOM
            nodes: List of nodes in the BOM tree
            edges: List of edges in the BOM tree
            view_id: ID of the view

        Returns:
            List of BOM instance data
        """
        parent_map = get_parent_map(edges)
        view_id = await self.get_default_view() if view_id is None else view_id

        return await asyncio.gather(
            *[
                self.get_instance(node.id, bom_id, view_id, parent_map.get(node.id))
                for node in nodes
                if node.group != "Bom"
            ]
        )

    async def load_bom_data(self, bom_id: str, view_id: str | None = None) -> dict:
        """Load BOM data.

        Args:
            bom_id: ID of the BOM
            view_id: ID of the view

        Returns:
            The formatted BOM data
        """
        bom, bom_tree = await asyncio.gather(
            self.get_bom(bom_id),
            self.get_bom_tree(bom_id, view_id),
        )
        instances = await self.get_bom_instances(
            bom_id=bom.id,
            view_id=view_id,
            nodes=bom_tree.nodes,
            edges=bom_tree.edges,
        )

        return format_bom(bom, instances)
