/**
 * Created with PyCharm.
 * User: ridhid
 * Date: 27.06.13
 * Time: 15:52
 * To change this template use File | Settings | File Templates.
 */

function Pagination(self) {
    self.page = ko.observable();
    this.previous = function() {
        if (self.page().previous) {
            var page = self.page();
            page.current = page.previous;
            self.page(page);
        }
    };
    this.next = function() {
        if (self.page().next) {
            var page = self.page();
            page.current = page.next;
            self.page(page);
        }
    };
    this.reset = function() {
        var page = self.page();
        page.current = 1;
        self.page(page);
    };
}

function Fs(self) {
    var local = this;
    self.dir = ko.observable();
    self.back_path = ko.observable();
    self.cwd = ko.observable("root");
    this.click = function(link) {
        if (link.url == null)
            local.into(link);
        else {
            self.video(false);
            self.video(link.url);
        }
    };
    this.into = function(folder) {
        self.pagination.reset();
        var cwd = self.cwd() == "root"? "" : self.cwd();
        self.cwd(cwd + '|' + folder.name);
    };
    this.to_root = function() {
        self.pagination.reset();
        self.cwd("root");
        console.log(self.cwd());
    };
    this.back_to = function(folder) {
        if (folder != "root")
            self.cwd(self.cwd().replace(new RegExp('(.*'+folder+').*', 'g'), '$1'));
        else
            local.to_root();
    };
}

function Navigation(self) {
    var local = this;
    self.default_visible = 'video';
    self.visible = ko.observable(self.default_visible);
    self.location_map = {
        record: 'record',
        config: 'settings/config',
        video: 'video'
    };
    this.record = function() {
        local.set_state('record');
    };
    this.config = function() {
        local.set_state('config');
    };
    this.video = function() {
        local.set_state('video');
    };
    this.set_state = function(state) {
        if ((state in self.location_map)) {
            self.location_hash(self.location_map[state]);
            self.visible(state);
        } else
            alert("Error! State not be unreachable");
    };
    self.location_hash = ko.computed({
        read: function() {
            var params = {
                cwd: self.cwd(),
                page: self.page()
            };
            if (params.page != null && params.cwd != null)
                location.hash = 'fs/' + params.cwd + '/' + params.page.current;
        },
        write: function(value) {
            location.hash = value;
        },
        owner: this
    });
}


function SideBar(self) {
    this.server_control = function(server) {
        var action = server.status === 'RUNNING' ? 'stop': 'start';
        $.get(control_url, {action: action}, function(data) {
            self.ajax.std_error(data);
            self.ajax.indo();
        });
    };
    this.server_control_restart = function() {
        $.get(control_url, {action: 'restart'});
    };
}


function Ajax(self) {
    var local = this;
    this.fs = function(sammy) {
        var path = sammy.params.path == "root" ? "" : sammy.params.path.replace(/\|/g, '/');
        $.get(url, {format: 'json', path: path, page: sammy.params.page}, function(data) {
            self.dir(data.dir);
            self.back_path(local.add_root(data.back_path));
            self.page(data.page);
        })
    };
    this.video = function() {
        $.getJSON(video_url, {format: 'json'}, function(data){
            self.rooms(data);
            Video = Refresher();
            Video.start(1000);
        });
    }
    this.add_root = function(bp) {
        return bp.reverse(), bp.push('root'), bp.reverse(), bp;
    };
    this.info = function() {
        $.get(info_url, function(data) {
            Model.info(data);
        });
    };
    this.config = function() {
        $.get(config_url, {action: 'static'} ,function(data) {
            self.config.add(data);
        });
    };
    this.save = function(item) {
        var params = {
            action: 'edit',
            section: item.section.name,
            option: item.header,
            value: item.value
        }
        $.get(config_url, params, function(data){
            local.std_error(data);
        });
        local.config()
    };
    this.delete = function(item) {
        var params = {
            action: 'delete',
            section: item.section.name,
            option: item.header
        };
        $.get(config_url, params, function(data){
            local.std_error(data);
        });
        local.config();
    };
    this.std_error = function(data) {
        if (data !== 'ok') {
            console.log('error', data)
        }
    };
}


function Config(self) {
    var local = this;
    self.cfg = ko.observableArray();
    self.edit = ko.observable(false);
    this.Item = function(item) {
        var self = this;
        this.Row = function(item, parent) {
            this.header = item.header;
            this.value = item.value;
            this.edit = local.edit;
            this.remove = local.delete;
            this.save = local.save;
            this.section = parent;
        };
        this.section = item.name;
        this.add_new = local.add_new;
        this.rows = item.items.map(function(item) {
            return new self.Row(item, self);
        }, item.items)
    };
    this.add = function(items) {
        var newItems = ko.utils.arrayMap(items, function(item) {
            return new local.Item(item);
        });
        self.cfg([]);
        self.cfg.pushAll(newItems);
    };
    this.edit = function(item) {
        self.edit(item);
        $('#editor').modal();
    };
    this.delete = function(item) {
        self.edit(false);
        self.ajax.delete(item);
    };
    this.save = function(item) {
        self.ajax.save(item);
    };
    this.add_new = function(section) {
        var new_instance = new section.Row({item: "", value: ""}, section);
        self.edit(new_instance);
        $('#editor').modal();
    }
}

function AppViewModel(){
    var self = this;

    this.video = ko.observable(false);
    this.info = ko.observable(false);

    this.pagination = new Pagination(self);
    this.fs = new Fs(self);
    this.navigation = new Navigation(self);
    this.sidebar = new SideBar(self);
    this.cams = new Cams(self)
    this.ajax = new Ajax(self);
    this.config = new Config(self);

    Sammy(function() {
        this.get('#fs/:path/:page', function() {
            self.ajax.fs(this);
            self.ajax.info();
        });
        this.get('#settings/config', function() {
            self.ajax.config();
        });
        this.get('#video', function() {
            self.ajax.video();
        })
    }).run('#video');
}

ko.observableArray.fn.pushAll = function(valuesToPush) {
    var underlyingArray = this();
    this.valueWillMutate();
    ko.utils.arrayPushAll(underlyingArray, valuesToPush);
    this.valueHasMutated();
    return this;
};

$(document).ready(function() {
    Model = new AppViewModel();
    ko.applyBindings(Model);
});