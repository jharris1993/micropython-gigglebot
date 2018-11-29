const jsonfile = require('jsonfile');
const fs = require('fs');
var lastTag = process.argv[2];

const file = '../changelog.json';
const output = '../tag';

console.log("checking a new version in changelogs")

jsonfile.readFile(file, function(err, changelogs) {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    
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
        var pos = 0;
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

    if (lastTag.major === winnerTag.major && lastTag.minor === lastTag.minor && lastTag.patch === lastTag.patch) {
        console.log('there\'s no tag in changelog higher than the latest one in the repo');
        process.exit(3);
    }

    fs.writeFile(output, `v${winnerTag.major}.${winnerTag.minor}.${winnerTag.patch}`, (err) => {
        if(err) {
            console.log(err);
            process.exit(4);
        }

        console.log(`new tag version got written to ${output} file`);
    });
})