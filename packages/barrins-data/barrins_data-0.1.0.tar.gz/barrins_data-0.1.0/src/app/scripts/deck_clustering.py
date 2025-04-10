import datetime

import numpy as np
from pydantic import BaseModel
from sklearn.cluster import KMeans as skKMeans
from sklearn.decomposition import PCA as skPca
from sklearn.metrics import silhouette_score

from src.app.models import DUEL_DATABASE
from src.app.mtg_formats import FORMATS
from src.app.scripts.deck_modelization import get_vector_from_decks
from src.app.scripts.deck_aggregation import aggregate_decks
from src.app.models.semantic_models import Decklist


class ClusteredDeck(BaseModel):
    deck_id: str
    player: str
    date: datetime.date
    cluster_id: int


class DeckCoordinates(BaseModel):
    id: str
    player: str
    date: datetime.date
    cluster: int
    x: float
    y: float


def clusters_map(
    format: str, with_aggregation: bool
) -> (
    dict[str, dict[str, DeckCoordinates | Decklist]]
    | dict[str, dict[str, list[DeckCoordinates]]]
):
    """Returns a mapping of decks to their clusters for a specific MTG format.

    Args:
        format (str): The MTG format to get the clusters map.
        with_aggregation (bool): Whether to aggregate the decks or not.

    Returns:
        dict[str, dict[str, DeckCoordinates | Decklist]] | dict[str, dict[str, list[DeckCoordinates]]]:
            If with_aggregation is True, returns a dictionary containing the aggregated decks.
            Otherwise, returns a list of DeckCoordinates objects.

    Raises:
        ValueError: If the format is not supported.
    """
    if format not in FORMATS:
        raise ValueError(f"Format {format} is not supported.")

    format_models = FORMATS.get(format)()

    with format_models.database.get_session() as session:
        decks = format_models.deck.get_decks_from_30_days(session)

        vectors = get_vector_from_decks(decks)
        pca_vectors = reduce_dimensions(vectors)
        labels = kmeans_clustering(pca_vectors)

        x_coord = pca_vectors[:, 0].tolist()
        y_coord = pca_vectors[:, 1].tolist()

        if format == "duel commander":
            with DUEL_DATABASE.get_session() as session:
                couples = [
                    ClusteredDeck(
                        deck_id=deck.str_commandzone,
                        cluster_id=cluster,
                        player=deck.player.name,
                        date=deck.in_tournament.date,
                    )
                    for deck, cluster in zip(decks, labels)
                ]
        else:
            couples = [
                ClusteredDeck(
                    deck_id=deck.id,
                    cluster_id=cluster,
                    player=deck.player.name,
                    date=deck.in_tournament.date,
                )
                for deck, cluster in zip(decks, labels)
            ]

        if with_aggregation:
            aggregated_decks = [
                (
                    i,
                    aggregate_decks(
                        [
                            deck.get_decklist()
                            for deck, cluster in zip(decks, labels)
                            if cluster == i
                        ],
                        order=1,
                    ),
                )
                for i in sorted(list(set(labels)))
            ]

    mapping = [
        DeckCoordinates(
            id=couple.deck_id,
            cluster=couple.cluster_id,
            x=x,
            y=y,
            player=couple.player,
            date=couple.date,
        )
        for couple, x, y in zip(couples, x_coord, y_coord)
    ]

    if with_aggregation:
        return {
            f"cluster_{i}": {
                "decklist": deck,
                "decks": [mapping for mapping in mapping if mapping.cluster == i],
            }
            for i, deck in aggregated_decks
        }

    return {
        f"cluster_{i}": {
            "decks": [maped for maped in mapping if maped.cluster == i],
        }
        for i in sorted(list(set(labels)))
    }


def reduce_dimensions(vectors: list, n_components: int = 2) -> list:
    """
    Reduce the dimensionality of the given vectors using PCA.

    Args:
        vectors (list): A list of vectors to reduce.
        n_components (int): The number of components to keep. Defaults to 2.

    Returns:
        list: A list of reduced vectors.

    Raises:
        ValueError: If the number of components is greater than the number of vectors.
    """
    if len(vectors[0]) < n_components:
        raise ValueError(
            f"The number of components ({n_components}) cannot exceed"
            + f" the number of features ({len(vectors[0])}) in the data."
        )

    pca = skPca(n_components=n_components)
    return pca.fit_transform(vectors)


def kmeans_clustering(vectors: list, random_state: int = 42):
    n_clusters = suggest_clusters(
        vectors=vectors,
        min_clusters=4,
        max_clusters=10,
        random_state=random_state,
    )

    kmeans = skKMeans(n_clusters=n_clusters, random_state=random_state)
    kmeans.fit(vectors)
    labels = [int(cluster) + 1 for cluster in kmeans.labels_]

    return labels


def suggest_clusters(
    vectors: list,
    min_clusters: int = 4,
    max_clusters: int = 10,
    random_state: int = 42,
) -> int:
    if len(vectors) < min_clusters:
        min_clusters = max(min_clusters, len(vectors))

    max_clusters = min(max_clusters, len(vectors))
    if min_clusters > max_clusters:
        max_clusters, min_clusters = min_clusters, max_clusters

    silhouette_scores = []

    for k in range(min_clusters, max_clusters + 1):
        kmeans = skKMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(vectors)
        score = silhouette_score(vectors, kmeans.labels_, random_state=random_state)
        silhouette_scores.append(score)

    return int(np.argmax(silhouette_scores)) + min_clusters
