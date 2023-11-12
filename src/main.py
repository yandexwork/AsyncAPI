from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, status, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.v1 import films, persons, genres
from core.config import settings
from db import elastic, redis
from limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])
    yield
    await redis.redis.close()
    await elastic.es.close()


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='localhost',
                agent_port=6831,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


configure_tracer()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


FastAPIInstrumentor.instrument_app(app)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
