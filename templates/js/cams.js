/**
 * Created with PyCharm.
 * User: ridhid
 * Date: 07.08.13
 * Time: 11:28
 * To change this template use File | Settings | File Templates.
 */
function Cam(src, name, row_begin) {
    this.src = src;
    this.name = name;
    this.row_begin = row_begin;
}

function Cams(self) {
    var local = this;
    self.rooms = ko.observable([]);
    self.zoom = ko.observable("");
    self.visible_cams = ko.observable([]);
    self.paginate_by = ko.observable();
    self.row = ko.observable();
    this.page = ko.observable();
    this.start_zoom = function(cam) {
        self.zoom(cam.src);
        $('#modal').modal();
    };
    this.stop_zoom = function(cam) {
        self.zoom("");
    };
    this.next_page = function() {
        local._computed_page(1);
    };
    this.prev_page = function() {
        local._computed_page(-1);
    };
    this._computed_page = function(value) {
        var page = local.page();
        var new_page = page + value;
        var diff = new_page - local.page();

        if (diff > 0 && local.has_next_page())
            local.page(new_page)
        else if (diff < 0 && local.has_prev_page())
            local.page(new_page)
    };
    this._paginate = ko.computed(function() {
        var page = local.page();
        var p_by = self.paginate_by();

        if (typeof(local.cams) != 'undefined')
            var cams_length = local.cams().length;
        else return; // not initialize depends objects

        var start = page * p_by;
        if (start < 0)
            start = 0;
        else if (start > cams_length)
            start = start - page > 0 && start - page < cams_length ? start - page : 0;

        var end = (page +1) * p_by;
        if (end >= cams_length || end < 0)
            end = cams_length;

        var visible_cams = local.cams().slice(start, end);
        self.visible_cams(visible_cams);
    }, this);
    this.has_next_page = function() {
        var page = local.page();
        var p_by = self.paginate_by();
        var cams_length = local.cams().length;

        var end = (page +1) * p_by;
        return !(end > cams_length || end < 0);
    };
    this.has_prev_page = function() {
        var page = local.page();
        var p_by = self.paginate_by();
        var cams_length = local.cams().length;

        var start = (page -1) * p_by;
        return !(start > cams_length || start < 0);
    }
    this.cams = ko.computed({
        read: function() {
            var params = {
                rooms: self.rooms()
            };

            var cams = [];
            params.rooms.forEach(function(room) {
                for (i=0 ; i < room.cams.length; i++) {
                    var row_begin = cams.length % self.row() ? false : true; // computed first element in string
                    var cam = new Cam(room.cams[i], room.name, row_begin);
                    cams.push(cam);
                }
            })
            return cams;
        },
        owner: this
    });
    this._init = function() {
        self.paginate_by(4);
        self.row(2);
        this.page(0);
    };
    this._init();
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

