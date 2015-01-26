angular.module('app', ['ngMaterial', 'ngCookies'])
    .factory('addToGCalendar', function ($http, $cookies, $q) {
        var token = $cookies.google_access_token;
        return function (groupName, cb) {
            $http.post('/api/kpi_schedule/', {group: groupName})
                .success(function (classes) {
                    console.log(classes);
                    var calendarId;
                    $http.post('https://www.googleapis.com/calendar/v3/calendars/?access_token=' + token, {
                        summary: "Розклад НТУУ \"КПІ\"",
                        description: "Автоматично створений розклад для НТУУ \"КПІ\"",
                        location: "НТУУ КПІ, Київ, Україна"
                    }).success(function (calendar) {
                        calendarId = calendar.id;
                        var ps = [];
                        for (var i = 0; i < classes.length; i++) {
                            var lesson = classes[i];
                            var secondSemester = moment().month() < 6;
                            var date = moment([moment().year(), secondSemester ? 1 : 8, 1, 8, 0]).day(lesson.day_number);
                            if (lesson.lesson_week === '2') {
                                date.add(7, 'day');
                            }
                            if (date.date() > 14 && !secondSemester) {
                                date.add(14, 'day');
                            }
                            var day = date.date();
                            var daystr = date.format('DD');
                            ps.push($http.post(
                                'https://www.googleapis.com/calendar/v3/calendars/' + 
                                    calendarId + '/events?access_token=' + token, {
                                    summary: lesson.lesson_name,
                                    description: lesson.lesson_name + ' (' + lesson.lesson_type + ')\n' +
                                        'Викладач: ' + lesson.teacher_name,
                                    start: {
                                        dateTime: moment().year() + (secondSemester ? '-02-' : '-09-') + daystr + 'T' + lesson.time_start,
                                        timeZone: 'Europe/Kiev'
                                    },
                                    end: {
                                        dateTime: moment().year() + (secondSemester ? '-02-' : '-09-') + daystr + 'T' + lesson.time_end,
                                        timeZone: 'Europe/Kiev'
                                    },
                                    recurrence: [
                                        "RRULE:FREQ=WEEKLY;INTERVAL=2;UNTIL=" + moment().year() +
                                            (secondSemester ? "0610" : "1231" ) + "T235959Z"
                                    ],
                                    location: "НТУУ КПІ (" + lesson.lesson_room + ")"
                            }));
                        }
                        $q.all(ps).then(function () {
                            cb(true);
                        }, function (err) {
                            cb(false);
                        });
                    }).error(function (err) {
                        cb(false);
                    })
                })
                .error(function (err) {
                    cb(false);
                });
        }
    })
    .controller('MainController', function ($scope, addToGCalendar, $cookies) {
        $scope.settings = $cookies;
    })
    .run(function($rootScope, $cookies, addToGCalendar) {
        if ($cookies.google_access_token) {
            addToGCalendar($cookies.groupName, function (result) {
                console.log('Result of adding to google calendar: ' + result);
                delete $cookies.google_access_token;
            });
        }
    });
