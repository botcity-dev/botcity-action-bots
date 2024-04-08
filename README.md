
<h1 align="center">
    <a href="">BotCity Actions - Bots</a>
</h1>

<p align="center">
  <a>
    <img alt="License" src=https://img.shields.io/hexpm/l/plug?style=for-the-badge>
  </a>
  <a>
    <img alt="Release" src=https://img.shields.io/github/v/release/botcity-dev/botcity-action-bots?style=for-the-badge>
  </a>
  <a href="https://join.slack.com/t/communitybotcitydev/shared_invite/zt-1ru3r3u2a-SsJL~w_7out3y7sEv3xC2w">
    <img alt="Slack" src="https://img.shields.io/badge/slack-join community-4A154B.svg?logo=slack&style=for-the-badge"/>
  </a>
  <a href="https://community.botcity.dev/">
    <img alt="Slack" src="https://img.shields.io/badge/forum-join forum-4A154B.svg?logo=discourse&style=for-the-badge"/>
  </a>
  <a href="https://www.youtube.com/@botcity-dev">
    <img alt="Slack" src="https://img.shields.io/badge/youtube-watch videos-4A154B.svg?logo=youtube&style=for-the-badge"/>
  </a>
</p>

<p align="center">
 <a href="##About">About</a> •
 <a href="##Usage">Usage</a> •
 <a href="##Support">Support</a> •
</p>

## 📚 About
This action makes automatic updates, deploys and releases to maestro, without the need for manual implementations.

It is possible to push an update to a specific branch or always upload a new version when a release is released in 
the project, it gives creativity and necessity.

## 💻 Usage
<!-- start usage -->
```yaml
name: Botcity Action
on: push

jobs:
  BotCity:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@master
        with:
          fetch-depth: 0
      - name: BotCity Action
        uses: botcity-dev/action@v1.0
        with:
          update: true
          deploy: false
          release: false
          version: 'v1.0'
          botId: 'botcityAction'
          technology: 'python'
          botPath: './bot.zip'
        env:
          LOGIN: ${{ secrets.LOGIN }}
          SERVER: ${{ secrets.SERVER }}
          KEY: ${{ secrets.KEY }}
```
<!-- end usage -->

### 🔣 Inputs
| Input             | Description                                                                                                                                                          | Default      |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| `technology`      | Technology used in the Bot. (Python, Java, Javascript, Typescript or Command.                                                                                        | **Required** |
| `botPath`         | Compressed file path. (zip or tar.gz)                                                                                                                                | **Required** |
| `update`          | Run update in Maestro.                                                                                                                                               | `false`      |
| `deploy`          | Execute deploy in Maestro.                                                                                                                                           | `false`      |
| `release`         | Release version to bot in Maestro                                                                                                                                    | `false`      |
| `version`         | Version of the action to run. If `version` is not set, the latest version is used in update. It is necessary to pass the version when performing deploy and release. | None         |
| `repositoryLabel` | This is the repository used at BotCity Orchestrator. Only use in Deploy.                                                                                             | DEFAULT      |


## ⛑ Support

### 📢 Join the community

If you have questions or comments in general about the plugin, we want to know.

You can choose between the channels the one that best fit you:

- [Forum BotCity Community](<https://community.botcity.dev>) (Public)
- [Slack BotCity Community](<https://join.slack.com/t/communitybotcitydev/shared_invite/zt-1ru3r3u2a-SsJL~w_7out3y7sEv3xC2w>) (Public)


## Contributing
### Bug Reports & Feature Requests

Please use the issue tracker to report any bugs or file feature requests.
Developing

### Local Development

Ready to contribute with code submissions and pull requests (PRs)? Here's how to set up BotCity action for local development.
1. Fork the repo
2. Clone the fork botcity-action repo locally
```shell
git clone git@github.com:botcity-dev/botcity-action.git
```
3. Create a branch for local development:
```shell
git checkout -b <name-of-your-branch>
```
4. Run command in source:
```shell
make dev
```
5. Verify changes locally run tests and linters:
```shell
make test
make format-code
make lint
```

6. Now you can make your changes locally.
```shell
git add .
git commit -m "Description of the changes goes here"
git push --set-upstream origin <name-of-your-branch>
```

7. It is only necessary to follow the template to create the pull request.

## Code of Conduct
To learn more about the code of conduct, access the following [documentation](<https://github.com/botcity-dev/code-of-conduct/blob/main/english.md>).
