# Conductor
📻 Written by &mdash; Andrew Codispoti, Adam Klen, Andrew McBurney, Dave Pagurek Van Mossel
___

### Development Setup

#### Mac Setup

1. Intstall brew
```shell
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

2. Install rbenv and other dependencies
```shell
brew install rbenv
brew install postgres
brew install redis
```

3. Start Postgres and Redis
```shell
brew services start postgresql
brew services start redis
```

4. Install nodejs, npm, and yarn
```shell
# Install nodejs and npm
brew install node

# Install yarn
brew install yarn
```

#### Ubuntu 16.04 Setup

1. Update apt-get
```shell
sudo apt-get update
```

2. Install dependencies for rbenv
```shell
sudo apt-get install autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3 libgdbm-dev
```

3. Install rbenv
```shell
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
```

4. Add `~/.rbenv/bin` to your `$PATH`
```shell
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
```

5. Install ruby-build for `rbenv install` command
```shell
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
```

6. Install nodejs, npm, and yarn
```shell
# Install nodejs
sudo apt-get install nodejs

# Install npm
sudo apt-get install npm

# Install yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
```

#### General Setup

1. Install Ruby 2.4.1
```shell
rbenv install 2.4.1
rbenv shell 2.4.1
rbenv rehash
```

2. Install bundler (package manager), and rubocop (linter)
```shell
gem install bundler
gem install rubocop
```

3. Install all dependencies
```shell
bundle install
```

4. Create development and test databases
```shell
bin/rails db:create
```

5. Start the server on http://localhost:5000/
```shell
foreman start
```

### Production Deploys

1. Add the heroku remote
```shell
heroku git:remote -a conductor-se464
```

2. Push your branch
```shell
git push heroku your_branch:master
```

### Program Output Server-Side
![Program Output](https://github.com/AndrewMcBurney/conductor/blob/master/app/assets/images/readme/flow.png)
