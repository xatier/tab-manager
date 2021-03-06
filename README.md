# Tab manager

Simple OneTab replacement.

## Why?

- OneTab is closed source
- JavaScript sucks
- I want to try out [FastAPI](https://fastapi.tiangolo.com/)

## Installation

1. Clone the repo to wherever-you-like
2. Navigate to `chrome://extensions` on Chromium
3. Load unpacked
4. Prepare python venv
5. Launch python server
6. You may want to change a few variables, such as timeout or save-path

```bash
cd tab-manager/tab-manager-server
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt

uvicorn server:app --reload --port 9487

# note that the chromium extension would automatically save all tabs once every hour
```

## See also

- [OneTab](https://www.one-tab.com/)
- [workona](https://workona.com/)

## Icon

Someone draw me one, please.

## Development

The chrome extension part uses [ESLint](https://eslint.org/) and [Prettier](https://prettier.io/) as linter and formatter, run commands below to install them:

```bash
$ npm install -g eslint prettier
# or
$ yarn global add eslint prettier
```

## Special thanks

[@david50407](https://github.com/david50407) helped me on crappy JavaScript issues.
