import os
from dotenv import load_dotenv


def test_env_variables_are_loaded(tmp_path, monkeypatch):
    
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=sk-test-key\nSERPAPI_API_KEY=serp-test-key\n")

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("SERPAPI_API_KEY", raising=False)

    load_dotenv(dotenv_path=str(env_file), override=True)

    assert os.getenv("OPENAI_API_KEY") == "sk-test-key"
    assert os.getenv("SERPAPI_API_KEY") == "serp-test-key"
