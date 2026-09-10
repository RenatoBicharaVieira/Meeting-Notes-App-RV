"""Developer-only local sign-in; the token is never a command argument or log."""
from getpass import getpass
from local_runtime import configure

configure()
from huggingface_hub import login

if __name__ == '__main__':
    print('Create a read token at https://huggingface.co/settings/tokens')
    print('Accept Community-1 access conditions in the same account first.')
    print('The token is saved only in ignored data/huggingface; never ship that folder.')
    token = getpass('Hugging Face read token (input hidden): ')
    try:
        login(token=token.strip(), add_to_git_credential=False)
        print('Local sign-in complete. You can close this terminal.')
    except Exception:
        print('Sign-in failed. Check the token and your network connection.')
        raise SystemExit(1)
    finally:
        token = None
