from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class SuapOAuth2Adapter(OAuth2Adapter):
    provider_id = "suap"
    settings = app_settings.PROVIDERS.get(provider_id, {})

    if "SUAP_URL" in settings:
        web_url = settings.get("SUAP_URL").rstrip("/")
        api_url = f"{web_url}/api"
    else:
        web_url = "https://suap.ifrn.edu.br"
        api_url = "https://suap.ifrn.edu.br/api"

    access_token_url = f"{web_url}/o/token/"
    authorize_url = f"{web_url}/o/authorize/"
    profile_url = f"{api_url}/rh/eu/"

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {token.token}"}
        resp = (
            get_adapter().get_requests_session().get(self.profile_url, headers=headers)
        )
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(SuapOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SuapOAuth2Adapter)
