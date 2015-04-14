# Travis VK Notificator
Travis-ci notificator for vk.com

## How do I get it?
It's pretty easy, just add http://travisnotificator-queyenth.rhcloud.com/?ids= {here the list of VK ids with comma separator}&format={here you can specify format for notification} to your webhooks notifications in travis.yml  
Example: [travis.yml](https://github.com/queyenth/PlatokGE/blob/develop/.travis.yml#L35)

## Format? Whaaat?
Ok, here the list of supporting variables:
* $c - commit hash
* $n - build number
* $o - owner of repo
* $m - commit message of build
* $s - status message of build
* $r - repository name
* $rid - repository id
* $bid - build id
* $rurl - repository url
* $burl - build url
* $started - started build time
* $finished - finished build time
* $duration - duration of build
* $branch - repository branch
* $compareurl - compare commit url
* $commitername - commiter name
* $commitermail - commiter mail
* $tag - tag
* $pullrequest - pull request
* $pullrequestnum - pull request number
* $pullrequesttitle - pull request title

Standard format: $o/$r build number #$n: $s\ncommit: $m\n$burl

## Didn't get an notification! Alarm!
Okay, first of all, check your privacy settings on your VK page, maybe only your friends can send you a private message. If so, please add [Travis](https://vk.com/id299973227) to your friends, or change your privacy settings.
