# decorators.py
import functools
import inspect
from opentelemetry import trace, metrics

from enum import Enum

class StepType(Enum):
    LLM = "llm"
    EMBEDDING = "embedding"
    SEMANTIC_SEARCH = "semantic_search"
    TOOL_CALL = "tool_call"


def workflow(_func=None, *, name=None):
    """
    Decorator to mark a function as a workflow, with optional override for span name.
    Usage:
        @workflow
        def my_workflow(): ...
        
        @workflow(name="CustomWorkflowName")
        def my_other_workflow(): ...
    """
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            meter = metrics.get_meter_provider().get_meter(__name__)
            function_call_counter = meter.create_counter(
                name="evalbase.function.calls",
                description="Counts function calls for evalbase telemetry decorators",
                unit="1"
            )

            # If a custom name was provided, use it; otherwise, use the function name
            span_name = name or func.__name__

            with tracer.start_as_current_span(span_name, record_exception=True) as span:
                span.set_attribute("function.args", str(args))
                span.set_attribute("function.kwargs", str(kwargs))
                result = func(*args, **kwargs)
                span.set_attribute("function.return", repr(result))
                function_call_counter.add(1, {"function.name": span_name, "function.type": "workflow"})
                return result

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            meter = metrics.get_meter_provider().get_meter(__name__)
            function_call_counter = meter.create_counter(
                name="evalbase.function.calls",
                description="Counts function calls for evalbase telemetry decorators",
                unit="1"
            )

            span_name = name or func.__name__

            with tracer.start_as_current_span(span_name, record_exception=True) as span:
                span.set_attribute("function.args", str(args))
                span.set_attribute("function.kwargs", str(kwargs))
                result = await func(*args, **kwargs)
                span.set_attribute("function.return", repr(result))
                function_call_counter.add(1, {"function.name": span_name, "function.type": "workflow"})
                return result

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    # If @workflow was used with parentheses (e.g. @workflow(name="myFlow")),
    # _func is None and we return the real decorator.
    # If @workflow was used without parentheses (e.g. @workflow), _func is the function,
    # so we apply the decorator directly.
    if _func is not None:
        return decorator(_func)
    else:
        return decorator


def step(_func=None, *, type: StepType = None, name=None):
    """
    Decorator for marking 'step' functions. Optionally specify:
      - type: A StepType enum to categorize the step, e.g. StepType.LLM
      - name: An explicit span name to override the default (the function name)
    Usage:
        @step
        def my_step(): ...

        @step(type=StepType.LLM)
        def llm_step(...): ...

        @step(name="CustomStepName")
        def named_step(...): ...

        @step(name="EmbeddingStep", type=StepType.EMBEDDING)
        def embedding_step(...): ...
    """
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            meter = metrics.get_meter_provider().get_meter(__name__)
            function_call_counter = meter.create_counter(
                name="evalbase.function.calls",
                description="Counts function calls for evalbase telemetry decorators",
                unit="1"
            )

            # If a custom name was provided, use it; otherwise, use the function name
            span_name = name or func.__name__

            with tracer.start_as_current_span(span_name, record_exception=True) as span:
                # Record the step type if provided
                if type:
                    span.set_attribute("step.type", type.value)

                span.set_attribute("function.args", str(args))
                span.set_attribute("function.kwargs", str(kwargs))
                result = func(*args, **kwargs)
                span.set_attribute("function.return", repr(result))

                function_call_counter.add(1, {
                    "function.name": span_name,
                    "function.type": "step",
                    "step.type": type.value if type else "none"
                })

                return result

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            meter = metrics.get_meter_provider().get_meter(__name__)
            function_call_counter = meter.create_counter(
                name="evalbase.function.calls",
                description="Counts function calls for evalbase telemetry decorators",
                unit="1"
            )

            span_name = name or func.__name__

            with tracer.start_as_current_span(span_name, record_exception=True) as span:
                if type:
                    span.set_attribute("step.type", type.value)

                span.set_attribute("function.args", str(args))
                span.set_attribute("function.kwargs", str(kwargs))
                result = await func(*args, **kwargs)
                span.set_attribute("function.return", repr(result))

                function_call_counter.add(1, {
                    "function.name": span_name,
                    "function.type": "step",
                    "step.type": type.value if type else "none"
                })

                return result

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    # If @step was used with parentheses (e.g. @step(type=StepType.LLM, name="Custom")),
    # _func is None and we return the real decorator.
    # If @step was used without parentheses (e.g. @step), _func is the function,
    # so we apply the decorator directly.
    if _func is not None:
        return decorator(_func)
    else:
        return decorator