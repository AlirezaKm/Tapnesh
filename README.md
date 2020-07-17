# Tapnesh Bot
Tapnesh Bot will optimize your images in parallel easily and efficiently! 
Tapnesh is only a wrapper to optimize images using `jpegoptim` for jpe?g and `pngquant` for png files in parallel using `parallel` package.

🤖 is available at [🔗 here](https://t.me/tapneshbot)


Docker
---
1. We need to build an image from our content:
`docker build -t tapnesh .`

2. Run a container from created image:
```bash
docker run -itd \
    -e TOKEN="<TELEGRAM_TOKEN>" \
    -e WEB_HOOK="<0 or 1>" \
    -e PORT="<PORT>" \
    -e DOMAIN="<WEB_HOOK_DOMAIN>" \
    tapnesh
```

3. Now you can communicate with your bot 🙂.

Heroku
---
In order to use this container in the [Heroku](https://heroku.com) follow the below steps:

1. Change the `stack` of the your application in the heroku to `container` with the following command:

```bash
heroku stack:set container -a <APP_NAME>
```

2. Set your variables in the environment at the heroku dashboard in the settings tab of your application:
```
TOKEN=<TOKEN>
WEB_HOOK=1
DOMAIN=https://<your-application-name>.herokuapp.com/
```

**NOTE**: the `PORT` variable will be selected by heroku.

2. Create a `heroku.yml` file and paste the below content into it:

```yaml
build:
  docker:
    web: Dockerfile
```

3. Add, Commit and push new file to the heroku.
```bash
# add files to git stage
git add -A .

# commit your changes
git commit -am 'heroku.yml added.'

# push to heroku master branch
git push heroku master
```

*NOTE 1*: if you want to use polling mode (set `WEB_HOOK=0` in the environment) for your telegram bot you need to replace `build.docker.web` section with `build.docker.worker` in `heroku.yaml` file.

*NOTE 2*: Don't forget to enable the worker (or web) in the heroku dashboard.


Installation
===
Just run this in your terminal    
`curl -Ss https://raw.githubusercontent.com/JafarAkhondali/Tapnesh/master/install.sh | bash`


Dependencies
---
```
pngquant
parallel
jpegoptim
```

Demo
---

Before Optimization ( Size: 4.1m )
![Before](https://user-images.githubusercontent.com/11364402/49339239-3e67d000-f644-11e8-91b8-5985b66880d0.jpg)


After Optimization ( `-q 45` Size: 1014kb )
![After](https://user-images.githubusercontent.com/11364402/49339240-3e67d000-f644-11e8-9793-d609f6f1fb42.jpg)


Examples
---
Optimize single image   
`tapnesh -p img.png`

Optimize single image with 75% of quality   
`tapnesh -p img.png -q 75`

Optimize whole directory with 85% of quality    
`tapnesh -p mydir -R -q 85`


Optimize whole directory and keep old files with 85% of quality    
`tapnesh -p mydir -R -q 85 -k `

Optimize image and keep old file     
`tapnesh -p img.jpg -k `


Options
---

```
Tapnesh is wrapper for image optimizers, It simply lets you optimize images in directory(ies) or single images in parallel
Usage: /usr/local/bin/tapnesh [-q|--quality <arg>] [-p|--path <arg>] [-R|--(no-)recursive] [-v|--(no-)verbose] [-k|--(no-)keep] [-h
|--help]
        -q,--quality: Sets quailty for optimized images, can be a value from 1 to 100. (100 means loseless optimization) (default:

'85')
        -p,--path: Path to directory for optimization (default: '.')
        -R,--recursive,--no-recursive: Do recursive (off by default)
        -v,--verbose,--no-verbose: Be verbose (off by default)
        -k,--keep,--no-keep: Keep old files (off by default)
        -h,--help: Prints help
```