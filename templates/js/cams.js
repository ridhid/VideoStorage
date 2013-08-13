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

function CamsGrid(row, cams) {
    this.grid = [];
    this._fill = function(row, cams) {
        var gs = function(i, row) {return i *row};
        var ge = function(i, row) {return (i + 1) * row};

        if(typeof(row) === 'string')
            row = row * 1

        console.log(cams.length - cams.length % row, row, cams.length % row)
        var block_size = cams.length % row ? (cams.length - cams.length % row) / row +1 : cams.length / row;

        for (var i = 0; i < block_size; i++ ) {
            var start, end;
            start = gs(i, row);
            end = ge(i, row);

            this.grid.push(cams.slice(start, end));
        }
    }
    this._fill(row, cams);
}

function Cams(self) {
    var local = this;
    self.rooms = ko.observable([]);
    self.zoom = ko.observable("");
    self.cams_grid = ko.observable([]);
    self.paginate_by = ko.observable();
    self.row = ko.observable();
    this.page = ko.observable();
    this.start_zoom = function(cam) {
        self.zoom(cam);
        $('#zoom_modal').modal();
    };
    this.stop_zoom = function(cam) {
        self.zoom(false);
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

        var cams = local.cams().slice(start, end);
        var grid = new CamsGrid(self.row(), cams);

        self.cams_grid(grid);
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
    this.show_settings = function() {
        $('#settings_modal').modal('show');
    }
    this.get_class = function(cam) {
        var out;
        var row = self.row() * 1;

        switch (row) {
            case 2:
                out = cam.row_begin ? 'col-lg-5 col-lg-offset-1 well' : 'col-lg-5 well';
                break;
            case 3:
                out = cam.row_begin ? 'col-lg-3 col-lg-offset-1 well' : 'col-lg-3 well';
                break;
            case 4:
                out = cam.row_begin ? 'col-lg-3 well' : 'col-lg-3 well';
                break;
            case 5:
                out = cam.row_begin ? 'col-lg-2 well col-lg-offset-1' : 'col-lg-2 well';
                break;
            case 6:
                out = cam.row_begin ? 'col-lg-2 well' : 'col-lg-2 well';
                break;
            default:
                break;
        }
        return out;
    }
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
            // выравнивание высоты \ иширны
            var parent_width = self.parent().width();
            self.width(parent_width);
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

