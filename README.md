# Conductor

## Development Setup

### Mac Setup
_Skip if not on Mac_

1. Intstall brew
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

2. Install rbenv
```shell
brew install rbenv
```

3. Install Ruby 2.4.1
```shell
rbenv install 2.4.1
rbenv shell 2.4.1
rbenv rehash
```

4. Install bundler (package manager), and rubocop (linter)
```shell
gem install bundler
gem install rubocop
```

### Linux Setup
_Skip if not on Linux_

1.

### General Setup

1. Install all dependencies
```shell
bundle install
```

2. Create development and test databases
```shell
rake db:create
```

3. Start the server on port 5000
```shell
foreman start
```

## Program Output Server-Side
![Program Output](https://github.com/AndrewMcBurney/conductor/blob/master/app/assets/images/readme/flow.png)
