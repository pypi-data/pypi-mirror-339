import argparse
import logging
from typing import Iterator, Optional

import grpc
import soundfile
import ubjson
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToJson
from phonexia.grpc.common.core_pb2 import (
    Audio,
    RawAudioConfig,
    TimeRange,
    Voiceprint,
)
from phonexia.grpc.technologies.age_estimation.v1.age_estimation_pb2 import (
    EstimateConfig,
    EstimateRequest,
)
from phonexia.grpc.technologies.age_estimation.v1.age_estimation_pb2_grpc import (
    AgeEstimationStub,
)

MAX_BATCH_SIZE = 1024


def time_to_duration(time: float) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def parse_vp(path: str) -> Voiceprint:
    with open(path, mode="rb") as file:
        return Voiceprint(content=file.read())


def is_ubjson_file(file_path):
    try:
        with open(file_path, "rb") as f:
            ubjson.load(f)
        return True  # noqa: TRY300
    except Exception:  # noqa: S110
        pass

    try:
        with open(file_path, "rb") as f:
            if f.read(4) == b"VPT ":
                return True
    except Exception:  # noqa: S110
        pass

    return False


def make_vp_batch_request(vp_list: Iterator[str]) -> Iterator[EstimateRequest]:
    batch_size = 0
    request = EstimateRequest()
    for vp_file in vp_list:
        if batch_size >= MAX_BATCH_SIZE:
            yield request
            batch_size = 0
            request = EstimateRequest()
        if vp_file:
            vp = parse_vp(vp_file)
            request.voiceprints.append(vp)
            batch_size += 1
    if len(request.voiceprints):
        yield request


def make_audio_batch_request(
    file: str,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    use_raw_audio: bool,
) -> Iterator[EstimateRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = EstimateConfig(speech_length=time_to_duration(speech_length))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                yield EstimateRequest(
                    audio=Audio(
                        content=data.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=config,
                )
                time_range = None
                raw_audio_config = None

    else:
        with open(file, mode="rb") as fd:
            while chunk := fd.read(chunk_size):
                yield EstimateRequest(
                    audio=Audio(content=chunk, time_range=time_range), config=config
                )
                time_range = None


def estimate_age(
    file: str,
    channel: grpc.Channel,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
):
    if is_ubjson_file(file):
        batch_request = make_vp_batch_request(iter([file]))
    else:
        batch_request = make_audio_batch_request(
            file=file,
            start=start,
            end=end,
            speech_length=speech_length,
            use_raw_audio=use_raw_audio,
        )

    stub = AgeEstimationStub(channel)
    for result in stub.Estimate(batch_request, metadata=metadata):
        print(MessageToJson(result, preserving_proto_field_name=True))


def main():
    parser = argparse.ArgumentParser(
        description="Age Estimation gRPC client. Estimate age from input voiceprints or audio file.",
    )
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="Voiceprint or audio to estimate age from"
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument(
        "--metadata",
        metavar="key=value",
        nargs="+",
        type=lambda x: tuple(x.split("=")),
        help="Custom client metadata",
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection.")
    parser.add_argument("--start", type=float, help="Audio start time in seconds.")
    parser.add_argument("--end", type=float, help="Audio end time in seconds.")
    parser.add_argument("--speech_length", type=float, help="Maximum amount of speech in seconds.")
    parser.add_argument("--use_raw_audio", action="store_true", help="Send raw audio.")
    args = parser.parse_args()

    if not args.file:
        raise ValueError("Parameter --file must not be an empty string")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")
    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")
    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")
    if args.speech_length is not None and args.speech_length <= 0:
        raise ValueError("Parameter 'speech_length' must be a float larger than 0.")

    try:
        logging.info(f"Connecting to {args.host}")
        channel = (
            grpc.secure_channel(target=args.host, credentials=grpc.ssl_channel_credentials())
            if args.use_ssl
            else grpc.insecure_channel(target=args.host)
        )
        estimate_age(
            file=args.file,
            channel=channel,
            metadata=args.metadata,
            start=args.start,
            end=args.end,
            speech_length=args.speech_length,
            use_raw_audio=args.use_raw_audio,
        )
    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)
    finally:
        channel.close()


if __name__ == "__main__":
    main()
