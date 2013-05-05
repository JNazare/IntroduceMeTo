// npm install rem async
var rem = require('rem')
  , async = require('async')
  , mongojs = require('mongojs')
  , fs = require('fs');

var db = mongojs('introducemeto', ['linkedin']);
 
// Create Facebook API, prompting for key/secret.
// Authenticate user via the console.
var linkedin = rem.connect('linkedin.com', 1.0).configure({
  key: process.env.LI_KEY,
  secret: process.env.LI_SECRET
});

function trimProfile (json) {
  return {
    "_id": json.id,
    "name": json.formattedName || '',
    "full_name": [json.firstName, json.lastName].join(' '),
    "headline": json.headline || '',
    "interests": json.interests || '',
    "positions": ((json.positions || {}).values || []).map(function (pos) {
      return [(pos.company || {}).industry, (pos.company || {}).name, pos.summary].join(', ')
    }).join('\n'),
    "url": json.publicProfileUrl
    // "skills": ((json.skills || {}).values || []).map(function (skill) {
      // return (skill.skill || {}).name;
    // }).join(', '),
    // "educations": ((json.educations || {}).values || []).map(function (edu) {
      // return [edu.degree, (edu.endDate || {}).year, edu.fieldOfStudy, edu.schoolName].join(', ')
    // }).join('\n'),
  }
}

// Read authentication for linkedin.
if (!fs.existsSync('cred.json')) {
  linkedin.promptAuthentication({
    scope: ['r_fullprofile', 'r_network']
  }, function (err, user) {
    user.saveState(function (state) {
      fs.writeFileSync('cred.json', JSON.stringify(state));
    });
  });

} else {
  var user = rem.oauth(linkedin).restore(JSON.parse(fs.readFileSync('cred.json')));

  user.debug = true;
 
  // Read our profile.
  fields = [
    'id', 'first-name', 'last-name', 'location:(name)', 'formatted-name', 'phone-numbers',
    'interests', 'headline', 'industry', 'current-share', 'summary', 'specialties',
    'positions', 'public-profile-url', 'publications', 'skills', 'educations', 'date-of-birth',
    'primary-twitter-account', 'twitter-accounts'
  ]
  user('people/~:(' + fields + ')').get(function (err, profile) {
    profile = trimProfile(profile);
    console.log(profile);
    db.linkedin.save(profile, console.error);
  });

  // Read connections.
  user('people/~/connections').get(function (err, json) {
    async.mapSeries(json.values.filter(function (conn) {
      // private profiles are private
      return conn.apiStandardProfileRequest;
    }), function (conn, next) {
      user('people/' + conn.id + ':(' + fields + ')').use(function (req, next) {
        for (var name in conn.apiStandardProfileRequest.headers.values) {
          req.headers[conn.apiStandardProfileRequest.headers.values[name].name] = conn.apiStandardProfileRequest.headers.values[name].value;
        }
        next()
      }).get(function (err, profile) {
        profile = trimProfile(profile);
        console.log(profile);
        db.linkedin.save(profile, console.error);

        next();
      });
    }, function (err, results) {
      console.log('done');
    });
  })
}