import re
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from vector_bridge import HTTPException
from vector_bridge.schema.helpers.enums import AIProviders, GPTActions


class FunctionsSorting(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class FunctionPropertyStorageStructure(BaseModel):
    name: str
    description: str
    type: str = Field(default="string")
    items: Dict[str, str] = Field(default_factory=dict)
    enum: List[str] = []
    required: bool = Field(default=False)


class FunctionParametersStorageStructure(BaseModel):
    properties: List[FunctionPropertyStorageStructure]

    def to_dynamodb_raw(self):
        return {
            "properties": {"L": [{"M": _property.to_dynamodb_raw()} for _property in self.properties]},
        }


class Overrides(BaseModel):
    ai_provider: Optional[AIProviders] = Field(default=None)
    model: str = Field(default="")
    system_prompt: str = Field(default="")
    message_prompt: str = Field(default="")
    knowledge_prompt: str = Field(default="")
    max_tokens: str = Field(default="")
    frequency_penalty: str = Field(default="")
    presence_penalty: str = Field(default="")
    temperature: str = Field(default="")


class Function(BaseModel):
    function_id: str
    function_name: str
    integration_id: str
    description: str
    accessible_by_ai: bool = Field(default=True)
    function_parameters: FunctionParametersStorageStructure
    overrides: Overrides = Field(default=Overrides())
    system_required: bool = Field(default=False)
    created_at: str = Field(default="")
    created_by: str = Field(default="")
    updated_at: str = Field(default="")
    updated_by: str = Field(default="")

    @property
    def uuid(self):
        return self.function_id

    @classmethod
    def to_valid_subclass(
        cls, data: dict
    ) -> Union[
        None,
        "OtherFunction",
        "CodeExecuteFunction",
        "SummaryFunction",
        "SemanticSearchFunction",
        "SimilarSearchFunction",
        "JsonFunction",
        "ForwardToAgentFunction",
    ]:
        function_action = data["function_action"]
        if function_action == GPTActions.SEARCH:
            return SemanticSearchFunction.model_validate(data)
        elif function_action == GPTActions.SIMILAR:
            return SimilarSearchFunction.model_validate(data)
        elif function_action == GPTActions.SUMMARY:
            return SummaryFunction.model_validate(data)
        elif function_action == GPTActions.JSON:
            return JsonFunction.model_validate(data)
        elif function_action == GPTActions.CODE_EXEC:
            return CodeExecuteFunction.model_validate(data)
        elif function_action == GPTActions.FORWARD_TO_AGENT:
            return ForwardToAgentFunction.model_validate(data)
        elif function_action == GPTActions.OTHER:
            return OtherFunction.model_validate(data)


class SemanticSearchFunction(Function):
    function_action: GPTActions = GPTActions.SEARCH
    vector_schema: str


class SimilarSearchFunction(Function):
    function_action: GPTActions = GPTActions.SIMILAR
    vector_schema: str


class SummaryFunction(Function):
    function_action: GPTActions = GPTActions.SUMMARY


class JsonFunction(Function):
    function_action: GPTActions = GPTActions.JSON


class CodeExecuteFunction(Function):
    function_action: GPTActions = GPTActions.CODE_EXEC
    code: str


class ForwardToAgentFunction(Function):
    function_action: GPTActions = GPTActions.FORWARD_TO_AGENT


class OtherFunction(Function):
    function_action: GPTActions = GPTActions.OTHER


class FunctionCreate(BaseModel):
    function_name: str
    description: str
    accessible_by_ai: bool = Field(default=True)
    function_parameters: FunctionParametersStorageStructure
    overrides: Overrides = Field(default=Overrides())


class SemanticSearchFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.SEARCH
    vector_schema: str


class SimilarSearchFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.SIMILAR
    vector_schema: str


class SummaryFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.SUMMARY


class JsonFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.JSON


class CodeExecuteFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.CODE_EXEC
    code: str


class FunctionUpdate(BaseModel):
    description: str
    accessible_by_ai: bool = Field(default=True)
    function_parameters: FunctionParametersStorageStructure
    overrides: Overrides = Field(default=Overrides())


class SemanticSearchFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.SEARCH
    vector_schema: str


class SimilarSearchFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.SIMILAR
    vector_schema: str


class SummaryFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.SUMMARY


class JsonFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.JSON


class CodeExecuteFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.CODE_EXEC
    code: str


class PaginatedFunctions(BaseModel):
    functions: List[
        Union[
            SemanticSearchFunction,
            SimilarSearchFunction,
            SummaryFunction,
            JsonFunction,
            CodeExecuteFunction,
            ForwardToAgentFunction,
            OtherFunction,
        ]
    ] = Field(default_factory=list)
    limit: int
    last_evaluated_key: Optional[str] = None
    has_more: bool = False

    @classmethod
    def resolve_functions(cls, data: dict) -> "PaginatedFunctions":
        functions = [Function.to_valid_subclass(func) for func in data["functions"]]
        data["functions"] = functions
        return PaginatedFunctions(**data)


class StreamingResponse:
    """
    Processes a binary stream, filtering out <ignore> messages and
    capturing everything inside <response>...</response>. If an <error>...</error>
    message is found, it returns the error instead.
    """

    RESPONSE_START = [b"<response>", b"<response>\n"]
    RESPONSE_END = [b"</response>", b"\n</response>"]
    ERROR_PATTERN = re.compile(rb"<error>(.*?)</error>", re.DOTALL)  # Regex for error messages
    MESSAGE_PATTERN = re.compile(rb"<response>\n(.*?)\n</response>", re.DOTALL)  # Regex for inline messages

    def __init__(self, stream):
        """
        Initializes the processor with a binary stream (generator).
        :param stream: An iterable or generator that yields binary messages.
        """
        self.stream = stream
        self.in_response_block = False  # Tracks if we're inside <response>...</response>
        self.buffer = []  # Stores accumulated response lines

    def response(self) -> Union[str, None]:
        """
        Processes the stream, returning the full data inside <response>...</response>.
        If an <error>...</error> message is found, it returns the error instead.
        """
        for message in self.stream:
            if not isinstance(message, bytes):
                continue  # Ensure it's binary (shouldn't happen but for safety)

            if message == b"<ignore>\n":
                continue  # Ignore <ignore> messages

            # Detect inline <error>...</error> message using regex
            error_match = self.ERROR_PATTERN.search(message)
            if error_match:
                raise HTTPException(
                    status_code=400, detail=error_match.group(1).decode("utf-8").strip()
                )  # Extract and raise error

            # Detect inline <response>...</response> message using regex
            msg_match = self.MESSAGE_PATTERN.search(message)
            if msg_match:
                self.buffer.append(msg_match.group(1))
                self.in_response_block = False
                break

            # Handle response start
            if message in self.RESPONSE_START:
                self.in_response_block = True
                self.buffer = []  # Clear buffer for new response
                continue

            # Handle response end
            if message in self.RESPONSE_END:
                self.in_response_block = False
                break

            # Store content inside <response>...</response>
            if self.in_response_block:
                self.buffer.append(message)

        if self.buffer:
            combined_buffer = b"".join(self.buffer).decode("utf-8")  # Decode and return full response
            return combined_buffer.rstrip("\n")
        return None
