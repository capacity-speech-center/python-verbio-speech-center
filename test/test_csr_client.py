import sys
sys.path.insert(1, '../proto/generated')
import pytest
from unittest.mock import Mock
from helpers.csr_client import CSRClient
from helpers.common import VerbioGrammar, RecognizerOptions
from concurrent.futures import ThreadPoolExecutor
import speechcenter.stt.recognition_streaming_request_pb2 as request
import speechcenter.stt.recognition_streaming_response_pb2 as response


def test_recognition_full_flow():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.asr_version = "V2"
    options.topic = "GENERIC"
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()


def test_recognition_full_flow_exception():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.asr_version = "V1"
    executor = ThreadPoolExecutor()
    audio_resource = Mock()
    audio_resource.sample_rate = 8000
    mock_stub.StreamingRecognize.side_effect = Exception("Exception while sending audio")
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    with pytest.raises(Exception):
        client.send_audio()
        client.wait_for_response()


def test_recognition_full_flow_provider():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.provider = "deepgram"
    options.topic = "GENERIC"
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()


def test_recognition_sends_speech_complete_timeout():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.provider = "capacity"
    options.topic = "GENERIC"
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False
    options.speech_complete_timeout = 1200

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()

    config = client._messages[0][1].config
    assert config.configuration.speech_complete_timeout == 1200


def test_recognition_sends_topic_name():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.provider = "capacity"
    options.topic_name = "conversational_ai"
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()

    resource = client._messages[0][1].config.resource
    assert resource.topic_name == "conversational_ai"
    assert not resource.HasField("topic")


def test_recognition_still_sends_deprecated_topic():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.topic = "BANKING"
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()

    resource = client._messages[0][1].config.resource
    assert resource.topic == request.RecognitionResource.Topic.BANKING
    assert not resource.HasField("topic_name")


def test_recognition_with_grammar_ignores_speech_complete_timeout():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.provider = "capacity"
    options.grammar = VerbioGrammar(VerbioGrammar.URI, "test/grammar")
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False
    options.speech_complete_timeout = 1200

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()

    config = client._messages[0][1].config
    assert not config.HasField("configuration")


def test_recognition_without_speech_complete_timeout_leaves_it_unset():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.provider = "capacity"
    options.topic = "GENERIC"
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()

    config = client._messages[0][1].config
    assert not config.HasField("configuration")


def test_recognition_full_flow_grammar():
    mock_stub = Mock()
    options = RecognizerOptions()
    options.inactivity_timeout = 0.1
    options.asr_version = "V2"
    options.grammar = VerbioGrammar(VerbioGrammar.URI, "test/grammar")
    options.language = "en-US"
    options.label = "label"
    options.formatting = False
    options.diarization = False

    audio_resource = Mock()
    audio_resource.sample_rate = 16000
    audio_resource.audio = b'0000000000000000'

    executor = ThreadPoolExecutor()
    recognition_result = response.RecognitionResult(is_final=True)
    mock_response = response.RecognitionStreamingResponse(result=recognition_result)
    mock_stub.StreamingRecognize.return_value = [mock_response, mock_response]
    client = CSRClient(executor, mock_stub, options, audio_resource, "token")
    client.send_audio()
    client.wait_for_response()
