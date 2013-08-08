/**
 * Created with PyCharm.
 * User: ridhid
 * Date: 07.08.13
 * Time: 11:28
 * To change this template use File | Settings | File Templates.
 */

function Cams(self) {
    self.rooms = ko.observable();
    self.zoom = ko.observable("");
    this.start_zoom = function(cam) {
        self.zoom(cam);
        $('.modal').show();
    };
    this.stop_zoom = function(cam) {
        self.zoom("");
    };
}

function Refresher() {
    self = this;
    this.refresh = function() {
        $('.video').each(function() {
            var self = $(this);
            var old = self.attr('src');
            self.removeAttr('src');
            self.attr('src', old)
        });
    };
    this.start = function(interval) {
        self.timeId = setInterval(this.refresh, interval)
    };
    this.stop = function() {
        clearTimeout(self.timeId);
    };
    return this;
}

