const jsonfile = require('jsonfile');
const fs = require('fs');
var lastTag = process.argv[2];

var file = "";
var output = "";
var changelogMD = "";
var titleFile = "";

if (process.env.TRAVIS_BUILD_DIR !== undefined) {
    file = `${process.env.TRAVIS_BUILD_DIR}/integration/changelog.json`;
    output = `${process.env.TRAVIS_BUILD_DIR}/integration/tag`;
    changelogMD = `${process.env.TRAVIS_BUILD_DIR}/integration/changelog.md`;
    titleFile = `${process.env.TRAVIS_BUILD_DIR}/integration/title`;
} else {
    file = 'changelog.json';
    output = 'tag';
    changelogMD = 'changelog.md';
    titleFile = 'title';
}

console.log("checking a new version in changelogs")

jsonfile.readFile(file, function(err, changelogs) {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    
    // ###########################################
    // checking if there's a tag in the changelogs
    // with the version number higher than in git
    // ###########################################
    const tags = Object.keys(changelogs);
    var curatedTags = [];
    console.log("detected", tags, "in changelog.json");

    var organizeTagNumbers = (tag) => {
        for (var idx = 0; idx < tag.length; idx++) {
            tag[idx] = parseInt(tag[idx].split('.').join(''));
        }

        if (tag.length === 1) {
            return {
                major: tag[0],
                minor: 0,
                patch: 0
            };
        }
        else if(tag.length === 2) {
            return {
                major: tag[0],
                minor: tag[1],
                patch: 0
            };
        }
        else {
            return {
                major: tag[0],
                minor: tag[1],
                patch: tag[2]
            };
        }
    };
    
    var processTag = (tag) => {
        var groups = re.exec(tag);
        if (groups === null) {
            console.error('detected bad version tag', tag);
            process.exit(2);
        } else {
            groups = groups.slice(1,4);
            groups = groups.filter(item => item !== undefined);
        }

        return organizeTagNumbers(groups);
    };

    var getWinnerTag = (currentTag, changeLogTags) => {
        var highest = {
            major: 0,
            minor: 0,
            patch: 0
        };
        changeLogTags.push(currentTag);

        changeLogTags.forEach((tag) => {
            if (tag.major > highest.major) {
                highest = tag;
                return;
            }
            if (tag.major < highest.major) {
                return;
            }
            
            if (tag.minor > highest.minor) {
                highest = tag;
                return;
            }
            if (tag.minor < highest.minor) {
                return;
            }

            if (tag.patch > highest.patch) {
                highest = tag;
                return;
            }
            if (tag.patch < highest.patch) {
                return;
            }
        });
        
        return highest;
        
    };

    const re = new RegExp('^v(\\d+\\.)?(\\d+\\.)?(\\d+)$');
    tags.forEach((tag) => {
        const tagNumber = processTag(tag);
        console.log("parsed", tagNumber);
        curatedTags.push(tagNumber);
    });
    lastTag = processTag(lastTag);
    console.log('latest tag in the repo is', lastTag);

    const winnerTag = getWinnerTag(lastTag, curatedTags);
    console.log('highest tag of all (including the one in the repo) is', winnerTag);

    if (lastTag.major === winnerTag.major && lastTag.minor === winnerTag.minor && lastTag.patch === winnerTag.patch) {
        console.log('there\'s no tag in changelog higher than the latest one in the repo');
        process.exit(3);
    }

    // ###########################################
    // outputting to file the new version number
    // ###########################################
    var formattedTag = `v${winnerTag.major}.${winnerTag.minor}.${winnerTag.patch}`;
    fs.writeFile(output, formattedTag, (err) => {
        if(err) {
            console.log(err);
            process.exit(4);
        }

        console.log(`new tag version got written to ${output} file`);
    });

    var newVersion = changelogs[formattedTag];

    console.log(changelogs);

    // ###########################################
    // parsing the changelog.json file and then
    // outputting the formatted one to a markdown
    // ###########################################
    if(! newVersion.hasOwnProperty('title')) {
        console.log('no title property in changelogs for', formattedTag);
        process.exit(4);
    }

    // var recursivelyConstructMD = (body, msg, level) => {
    //     if(body.constructor == Array) {
    //         body.forEach((row) => {
    //             msg += `* ${row}\n`.padStart(level * 2, ' ');
    //         });
    //         console.log(msg);
    //         return msg;
    //     } else if (body.constructor == Object){
    //         Object.keys(body).forEach((key) => {
    //             console.log(body[key]);
    //             var addedBody = recursivelyConstructMD(body[key], msg + `${key}:\n`, level + 1);
    //             if (addedBody !== undefined) {
    //                 msg += addedBody;
    //                 msg += '\n';
    //             }
    //         });

    //         return msg;
    //     }
    // };
    var title = `${newVersion.title}`;
    var body = "";
    if(newVersion.hasOwnProperty('body')) {
        // check if newVersion.body is array
        if(newVersion.body.constructor == Array) {
            newVersion.body.forEach((row) => {
                body += `* ${row}\n`;
            });
        } else if(newVersion.body.constructor == Object) {
            Object.keys(newVersion.body).forEach((key) => {
                if(newVersion.body[key].constructor == Object) {
                    console.log('too many subpoints in the changelog');
                    process.exit(5);
                } else if (newVersion.body[key].constructor == Array && newVersion.body[key].length > 0) {
                    body += `${key}:\n`;
                    newVersion.body[key].forEach((row) => {
                        body += `* ${row}\n`;
                    });
                    body += '\n';
                }
            });
        }
        // body = recursivelyConstructMD(newVersion.body, '', 1);
    }  

    // ###########################################
    // writing the release title in a file and then
    // the release body in another markdown file
    // ###########################################

    fs.writeFile(changelogMD, body, (err) => {
        if(err) {
            console.log(err);
            process.exit(6);
        }

        console.log(`new changelog in md format got written to ${changelogMD} file`);
    });

    fs.writeFile(titleFile, title, (err) => {
        if(err) {
            console.log(err);
            process.exit(7);
        }

        console.log(`new title for release got written to ${titleFile} file`);
    });
})