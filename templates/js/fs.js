/**
 * Created with PyCharm.
 * User: ridhid
 * Date: 18.06.13
 * Time: 15:48
 * To change this template use File | Settings | File Templates.
 */

function AppViewModel(data) {
    var self = this;
    this.dir = ko.observable();
    this.back_path = ko.observable();
    this.page = ko.observable();
    this.cwd = ko.observable("root");
    this.video = ko.observable("");
    this.previous_page = function() {
        if (self.page().previous) {
            var page = self.page();
            page.current = page.previous;
            self.page(page);
        }
    };
    this.next_page = function() {
        if (self.page().next) {
            var page = self.page();
            page.current = page.next;
            self.page(page);
        }
    };
    this.reset_page = function() {
        var page = self.page();
        page.current = 1;
        self.page(page);
    }
    this.click = function(link) {
        if (link.url ==null)
            self.into(link);
        else {
            self.video(link.url)
            play();
        }
    },
    this.into = function(folder) {
        self.reset_page();
        var cwd = self.cwd() == "root"? "" : self.cwd()
        self.cwd(cwd + '|' + folder.name);
    };
    this.to_root = function() {
        self.reset_page();
        self.cwd("root");
    }
    this.back_to = function(folder) {
        self.cwd(self.cwd().replace(new RegExp('(.*'+folder+').*', 'g'), '$1'));
    }
    Sammy(function() {
        this.get('#video/:path/:page', function() {
            var path = this.params.path == "root" ? "" : this.params.path.replace(/\|/g, '/');
            $.get(url, {format: 'json', path: path, page: this.params.page}, function(data) {
                self.dir(data.dir);
                self.back_path(data.back_path);
                self.page(data.page);
            })
        });
    }).run('#video/root/1');
    this.location_hash = ko.computed(function() {
        var cwd = self.cwd();
        var page = self.page();
        if (page != null && cwd != null)
            location.hash = 'video/' + cwd + '/' + page.current;
    }, this)
}

$(document).ready(function() {
    Model = new AppViewModel();
    ko.applyBindings(Model);
});

function play() {
    projekktor(
        '#player',
        {
            controls: true,
            debug: false,
            loop: false,
            addplugins: ['display', 'controlbar']
        },
        function(player) { // "onready" callback -
            $('#projekktorver').html( player.getPlayerVer() );
        }
    );
}

