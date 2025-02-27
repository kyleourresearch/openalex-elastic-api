import json

from marshmallow import fields, INCLUDE, Schema, post_dump, pre_dump

from core.schemas import (
    CountsByYearSchema,
    GroupBySchema,
    GroupBysSchema,
    MetaSchema,
    TopicSchema,
    TopicHierarchySchema,
    hide_relevance,
    relevance_score,
)


class AuthorSchema(Schema):
    id = fields.Str()
    display_name = fields.Str()
    orcid = fields.Str()

    class Meta:
        ordered = True


class InstitutionsSchema(Schema):
    id = fields.Str()
    display_name = fields.Str()
    ror = fields.Str()
    country_code = fields.Str()
    type = fields.Str()
    lineage = fields.List(fields.Str())

    class Meta:
        ordered = True


class AffiliationsSchema(Schema):
    raw_affiliation_string = fields.Str()
    institution_ids = fields.List(fields.Str())

    class Meta:
        ordered = True


class AuthorshipsSchema(Schema):
    author_position = fields.Str()
    author = fields.Nested(AuthorSchema)
    institutions = fields.Nested(InstitutionsSchema, many=True)
    countries = fields.List(fields.Str())
    is_corresponding = fields.Bool()
    raw_author_name = fields.Str()
    raw_affiliation_strings = fields.List(fields.Str())
    affiliations = fields.Nested(AffiliationsSchema, many=True)

    class Meta:
        ordered = True


class BiblioSchema(Schema):
    volume = fields.Str()
    issue = fields.Str()
    first_page = fields.Str()
    last_page = fields.Str()

    class Meta:
        ordered = True


class ConceptsSchema(Schema):
    id = fields.Str()
    wikidata = fields.Str()
    display_name = fields.Str()
    level = fields.Int()
    score = fields.Float()

    class Meta:
        ordered = True


class CitationNormalizedPercentileSchema(Schema):
    value = fields.Float()
    is_in_top_1_percent = fields.Bool()
    is_in_top_10_percent = fields.Bool()

    class Meta:
        ordered = True


class GrantsSchema(Schema):
    funder = fields.Str()
    funder_display_name = fields.Str()
    award_id = fields.Str()

    class Meta:
        ordered = True


class SourceSchema(Schema):
    id = fields.Str()
    display_name = fields.Str()
    issn_l = fields.Str()
    issn = fields.List(fields.Str())
    is_oa = fields.Bool()
    is_in_doaj = fields.Bool()
    is_core = fields.Bool()
    host_organization = fields.Str()
    host_organization_name = fields.Str()
    host_organization_lineage = fields.List(fields.Str())
    host_organization_lineage_names = fields.List(fields.Str())
    type = fields.Str()

    class Meta:
        ordered = True


class LocationSchema(Schema):
    is_oa = fields.Bool()
    landing_page_url = fields.Str()
    pdf_url = fields.Str()
    source = fields.Nested(SourceSchema)
    license = fields.Str()
    license_id = fields.Str()
    version = fields.Str()
    is_accepted = fields.Bool()
    is_published = fields.Bool()

    class Meta:
        ordered = True


class OpenAccessSchema(Schema):
    is_oa = fields.Bool()
    oa_status = fields.Str()
    oa_url = fields.Str()
    any_repository_has_fulltext = fields.Bool()

    class Meta:
        ordered = True
        unknown = INCLUDE


class IDsSchema(Schema):
    openalex = fields.Str()
    doi = fields.Str()
    mag = fields.Str()
    pmid = fields.Str()
    pmcid = fields.Str()

    class Meta:
        ordered = True
        unknown = INCLUDE


class MeshSchema(Schema):
    descriptor_ui = fields.Str()
    descriptor_name = fields.Str()
    qualifier_ui = fields.Str()
    qualifier_name = fields.Str()
    is_major_topic = fields.Boolean()

    class Meta:
        ordered = True


class APCSchema(Schema):
    value = fields.Integer()
    currency = fields.Str()
    value_usd = fields.Integer()
    provenance = fields.Str()

    class Meta:
        ordered = True


class SDGSchema(Schema):
    id = fields.String()
    display_name = fields.String()
    score = fields.Float()


class CitedByPercentileYearSchema(Schema):
    min = fields.Integer()
    max = fields.Integer()

    class Meta:
        ordered = True


class KeywordsSchema(Schema):
    id = fields.String()
    display_name = fields.String()
    score = fields.Float()

    class Meta:
        ordered = True


class WorksSchema(Schema):
    id = fields.Str()
    doi = fields.Str()
    title = fields.Str()
    display_name = fields.Str()
    relevance_score = fields.Method("get_relevance_score")
    publication_year = fields.Int()
    publication_date = fields.Str()
    ids = fields.Nested(IDsSchema)
    language = fields.Str()
    primary_location = fields.Nested(LocationSchema)
    type = fields.Str()
    type_crossref = fields.Str()
    indexed_in = fields.List(fields.Str())
    open_access = fields.Nested(OpenAccessSchema)
    authorships = fields.Nested(AuthorshipsSchema, many=True)
    countries_distinct_count = fields.Int()
    institutions_distinct_count = fields.Int()
    corresponding_author_ids = fields.List(fields.Str())
    corresponding_institution_ids = fields.List(fields.Str())
    apc_list = fields.Nested(APCSchema, dump_default=None)
    apc_paid = fields.Nested(APCSchema, dump_default=None)
    fwci = fields.Float()
    is_authors_truncated = fields.Bool(attribute="authorships_truncated")
    has_fulltext = fields.Bool()
    fulltext_origin = fields.Str()
    cited_by_count = fields.Int()
    citation_normalized_percentile = fields.Nested(CitationNormalizedPercentileSchema)
    cited_by_percentile_year = fields.Nested(CitedByPercentileYearSchema)
    biblio = fields.Nested(BiblioSchema)
    is_retracted = fields.Bool()
    is_paratext = fields.Bool()
    primary_topic = fields.Nested(TopicSchema)
    topics = fields.Nested(TopicSchema, many=True)
    keywords = fields.Nested(KeywordsSchema, many=True)
    concepts = fields.Nested(ConceptsSchema, many=True)
    mesh = fields.List(fields.Nested(MeshSchema))
    locations_count = fields.Int()
    locations = fields.Nested(LocationSchema, many=True)
    best_oa_location = fields.Nested(LocationSchema)
    sustainable_development_goals = fields.Nested(SDGSchema, many=True)
    grants = fields.List(fields.Nested(GrantsSchema))
    datasets = fields.List(fields.Str())
    versions = fields.List(fields.Str())
    referenced_works_count = fields.Int()
    referenced_works = fields.List(fields.Str())
    related_works = fields.List(fields.Str())
    ngrams_url = fields.Method("get_ngrams_url")
    abstract_inverted_index = fields.Function(
        lambda obj: json.loads(obj.abstract_inverted_index).get("InvertedIndex")
        if "abstract_inverted_index" in obj and obj.abstract_inverted_index
        else None
    )
    cited_by_api_url = fields.Str()
    counts_by_year = fields.List(fields.Nested(CountsByYearSchema))
    updated_date = fields.Str()
    created_date = fields.Str(dump_default=None)

    @pre_dump
    def pre_dump(self, data, **kwargs):
        """If single record, display authorships_full rather than truncated list."""
        if "single_record" in self.context and self.context["single_record"]:
            if "authorships_full" in data:
                data.authorships = data.authorships_full
                del data.authorships_truncated
        return data

    @post_dump
    def remove_relevance_score(self, data, many, **kwargs):
        return hide_relevance(data, self.context)

    @staticmethod
    def get_relevance_score(obj):
        return relevance_score(obj)

    @staticmethod
    def get_ngrams_url(obj):
        short_id = obj.id.replace("https://openalex.org/", "")
        ngrams_url = f"https://api.openalex.org/works/{short_id}/ngrams"
        return ngrams_url

    class Meta:
        ordered = True


class MessageSchema(Schema):
    meta = fields.Nested(MetaSchema)
    results = fields.Nested(WorksSchema, many=True)
    group_by = fields.Nested(GroupBySchema, many=True)
    group_bys = fields.Nested(GroupBysSchema, many=True)

    class Meta:
        ordered = True
