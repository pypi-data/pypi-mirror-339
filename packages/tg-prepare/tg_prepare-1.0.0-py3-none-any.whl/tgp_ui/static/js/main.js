function loadTEIContent(e) {
    e.preventDefault();
    const self = $(this);
    const tab = self.closest('.tab-pane');

    // toggle classes to highlight selected row and XML element
    tab.find('.row.bg-light').removeClass('bg-light')
    tab.find('.bg-info').removeClass('bg-info')
    self.closest('.row').addClass('bg-light')
    self.addClass('bg-info')

    $.ajax({
        url: self.data('url'),
        method: 'GET',
        dataType: 'json',
        data: self.data(),
        success: function (response) {
            tab.find(".output").empty();
            var col = $('<div class="col"></div>');
            col.append('<h3>' + self.data('heading') + '</h3>');
            col.append('<span></span>');
            tab.find(".output").append(col);
            col.find('span').simpleXML({ xmlString: response.content });
        }
    });
};

const loadTEIExplorerTab = function (e) {
    const self = $(this);
    const tab = $(self.data('bs-target'));
    if (!tab.hasClass('loaded')) {
        tab.load(self.data('url'), function () {
            tab.addClass('loaded');
        })
    }
}

const showXPathInTEIExplorer = function (e) {
    const self = $(this);
    const form = self.closest('form');
    // fill xpath value into input field
    form.find('input[name=xpath]').val(self.data('xpath'));
    // trigger search for xpath
    form.find('.check-xpath').trigger('click');
    // open tei_explorer tab
    form.find('.tei_explorer').trigger('click');
}

const checkXPath = function (e) {
    e.preventDefault();
    const self = $(this);
    const tab = self.closest('form').find(
        '.tab-pane.tei-explorer-content.loaded');
    console.log(self.closest('.row').find('input[name=xpath]').val())
    $.ajax({
        url: self.data('url'),
        method: 'GET',
        dataType: 'json',
        data: { 'xpath': self.closest('.row').find('input[name=xpath]').val() },
        success: function (response) {
            // set '-' as default value (in case no result is found)
            tab.find('.xpath-result').text('-');
            response.results.forEach(function (d) {
                tab.find('[data-name="' + d.filename + '"]').text(d.result);
            })
        }
    });
}

const cloneFromGit = function (e) {
    e.preventDefault();
    var self = $(this);
    self.find('button')
        .removeClass('btn-danger')
        .addClass('btn-primary')
        .prop('disabled', true);
    self.find('button span').toggle();
    $.ajax({
        url: self.data('url'),
        method: 'POST',
        dataType: 'json',
        data: self.serialize(),
        success: function (response) {
            self.find('button').prop('disabled', false);
            self.find('button span').toggle();
            if (response.value == 'OK') {
                location.reload();
            }
        },
        error: function (response) {
            self.find('button').prop('disabled', false);
            self.find('button')
                .removeClass('btn-primary')
                .addClass('btn-danger');
            self.find('button span').toggle();
        }

    });
};

const showFiles = function (e) {
    e.preventDefault();
    $(this).closest('.folder').find('.file').toggle();
    $(this).find('span')
        .toggleClass('bi-eye-slash-fill bi-eye-fill');
};

const saveCollectionSettings = function (e) {
    e.preventDefault();
    var self = $(this);
    let data = {};

    self.find(':not(.no-serialization)').serializeArray().forEach(function (d) {
        data[d.name] = d.value;
    })

    // loop through multi-inputs
    self.find('.multi-input').each(function (i, d1) {
        console.log(d1)
        let multi_input = $(d1);
        if (data[multi_input.data('name')] === undefined) {
            data[multi_input.data('name')] = [];
        }
        // get all keys and values for each multi-input
        let item = {};
        multi_input.find('input').each(function (i, d2) {
            item[$(d2).data('key')] = $(d2).val();
        });
        data[multi_input.data('name')].push(JSON.stringify(item))
    })

    // loop throuh xpath-or-value-input
    let _data = {}
    self.find('.xpath-or-value-input input').each(function (i, d) {
        const xv_input = $(d);
        const xv_data = xv_input.data();
        const xv_name = xv_data['name'];
        if (_data[xv_name] === undefined) {
            _data[xv_name] = {};
        }
        _data[xv_name][xv_data['type']] = xv_input.val();
    })
    for (const [key, value] of Object.entries(_data)) {
        data[key] = JSON.stringify(value);
    }
    console.table(data)

    $.ajax({
        url: self.attr('action'),
        method: 'POST',
        dataType: 'json',
        data: data,
        success: function (response) {
            if (response.response == 'OK') {
                // trigger reload of tab content
                const target = $('.collection-tab.active').attr('href')
                $(target).attr('reload', true)
                loadCollectionTab.call($('.collection-tab.active')[0]);
            }
        }
    });
}

// NEXTCLOUD
// #######################

const selectNextcloudFolder = function (e) {
    e.preventDefault();
    const self = $(this);
    self.find('span.bi')
        .toggleClass('bi-circle-fill bi-circle');
}

const loginNextcloud = function (e) {
    e.preventDefault();
    const spinner = document.querySelector(".spinner-login");
    const error = document.getElementById("login-error");
    spinner.hidden = false;
    error.hidden = true;

    fetch('/nextcloud_login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: Object.fromEntries(new FormData(document.querySelector(".login"))) }),
    })
        .then(response => response.json())
        .then(() => _loadNextcloudTab('/nextcloud_tab'))
        .catch(() => (error.hidden = false))
        .finally(() => (spinner.hidden = true));
};

const processSelectionCloud = function (e) {
    const spinner = document.querySelector(".spinner-submit");
    spinner.hidden = false;

    const filePaths = Array.from(document.querySelectorAll('.nxc_select-folder > .bi.bi-circle-fill'))
        .map(path => path.dataset.path);
    const projectname = document.getElementById('tab_nextcloud').dataset.projectname;

    fetch('/nextcloud_download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_paths: filePaths, projectname }),
    })
        .then(response => response.json())
        .finally(() => (spinner.hidden = true));
};

// Function to handle logout from Nextcloud
const logoutNextcloud = function (e) {
    var self = $(this);
    // Send a POST request to the server to log out
    fetch('/nextcloud_logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.response === 'OK') {
                // If logout is successful, mark the Nextcloud tab as not loaded
                $('#tab_nextcloud').removeClass('loaded');
                // Reload the Nextcloud tab with the specified project name
                _loadNextcloudTab('/nextcloud_tab');
            }
        });
}

// Helper function to load the Nextcloud tab content
const _loadNextcloudTab = function (url) {
    // Check if the Nextcloud tab is already loaded
    if (!$('#tab_nextcloud').hasClass('loaded')) {
        // Show a loading spinner while the content is being fetched
        $('#tab_nextcloud').html('<div class="d-flex justify-content-center p-5"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>')
        // Send an AJAX request to load the tab content
        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'html',
            success: function (response) {
                // Populate the tab with the response and mark it as loaded
                $('#tab_nextcloud')
                    .html(response)
                    .addClass('active')
                    .show();
                if ($('#tab_nextcloud').find('#nextcloud_login').length == 0) {
                    $('#tab_nextcloud').addClass('loaded');
                }
            }
        });
    } else {
        // If the tab is already loaded, simply make it active and visible
        $('#tab_nextcloud').addClass('active').show();
    }
}

// Function to load the Nextcloud tab when triggered
const loadNextcloudTab = function (e) {
    const self = $(this);
    // Call the helper function to load the tab content
    _loadNextcloudTab(self.data('url'));
}

// #######################

const selectFolder = function (e) {
    e.preventDefault();
    const self = $(this);
    self.closest('.folder').toggleClass('bg-warning');
    self.find('span.bi')
        .toggleClass('bi-circle-fill bi-circle');
    const tab = self.closest('.tab-pane');
    const spinner = self.closest('.folder').find('.spinner-border');
    spinner.toggle();

    const data = tab.find('span.bi-circle-fill').map((i, d) => (
        { name: 'tei_directories', value: $(d).data('path') })).get();
    $.post({
        url: self.data('url'),
        dataType: 'json',
        data: data,
        success: (response) => {
            spinner.toggle();
            if (response.response === 'OK') {
                location.reload();
            }
        }
    });
};

const addMultiInput = function (e) {
    e.preventDefault();
    const self = $(this);
    const this_row = self.closest('.row')
    this_row.next().clone()
        .insertAfter(this_row)
        .find('input').val('');
}
const removeMultiInput = function (e) {
    e.preventDefault();
    const self = $(this);
    const this_multi_input = self.closest('.multi-input')
    this_multi_input.remove();
}

const loadCollectionTab = function (e) {
    const self = $(this);
    const tab = $(self.attr('href'));
    if (tab.find('form.collection-form').length === 0 || tab.attr('reload') === 'true') {
        tab.css('opacity', 0.5);
        tab.attr('reload', false)
        self.find('i').toggle();
        $('#tab_' + self.data('name')).load(
            self.data('url'),
            self.data(), function () {
                self.find('i').toggle();
                tab.css('opacity', 1);
            })
    }
}

// this function replaces (kind of) the normal submit
// by sending the form data via ajax and reloading the tab content
const tabSubmit = function (e) {
    e.preventDefault();
    const self = $(this);
    const submit_icons = self.find('button[type=submit] span');
    submit_icons.toggle();
    $.post(self.attr('action'), self.serialize(), function (response) {
        if (response.response === 'OK') {
            submit_icons.toggle();
            // console.log(response)
        }
    })
}

const selectTGProject = function (e) {
    e.preventDefault();
    const self = $(this);
    self.closest('.row').find('.bi-circle-fill').toggleClass('bi-circle-fill bi-circle');
    self.find('span')
        .addClass('bi-circle-fill')
        .removeClass('bi-circle');
    $.post(self.data('url'), self.data(), function (response) {
        if (response.response === 'OK') {
        }
    })
}

// get the hits of a project (recursively) until the spinner is no more visible
const getTGProjectHits = function (url, content, spinner) {
    // wait 10 seconds before sending the next request
    setTimeout(function () {
        $.get(url, function (response) {
            const fs = content.css('font-size');
            // show hits and (slightly) highlight the text
            content
                .animate({ fontSize: '18px' }, 'slow')
                .text(response.hits)
                .animate({ fontSize: fs }, 'slow');
            // check if spinner is still visible
            if (spinner.is(':visible') > 0) {
                // if so, trigger this function again
                getTGProjectHits(url, content, spinner);
            }
        })
    }, 10000);
}

const deleteTGProject = function (e) {
    e.preventDefault();
    const self = $(this);
    const spans = self.find('span');
    // show spinner & hide trash icon
    spans.toggle();
    // send delete request to server
    $.post(self.data('url'), function () {
        // hide spinner & show trash icon
        self.find('span').toggle();
    });
    // get the hits of the project
    getTGProjectHits(
        self.data('hits_url'), // url to get the hits
        self.closest('.tg-project-row').find('.tgProjectHits'), // content to show the hits
        self.find('.spinner-border') // spinner to check if it is still visible
    );
}

$(document).ready(function () {

    // ##SIDEBAR##
    document.querySelector(".toggle-btn").addEventListener("click", function () {
        document.querySelector("#sidebar").classList.toggle("expand");
    });

    // ##FILES VIEW##
    $('li.folder a.show-files').on('click', showFiles);
    $('li.folder a.select-folder').on('click', selectFolder);
    $(document).on('submit', 'form#cloneFromGit', cloneFromGit);
    $(document).on('submit', 'form#nextcloud_login', loginNextcloud);
    $(document).on('click', '#tab_nextcloud #nextcloud_logout', logoutNextcloud);
    $(document).on(
        'show.bs.tab', 'a[data-bs-toggle="tab"][aria-controls="tab_nextcloud"]',
        loadNextcloudTab);
    $(document).on('click', 'li.folder a.nxc_select-folder', selectNextcloudFolder);
    $(document).on('click', 'button.submit-selection', processSelectionCloud);

    // ##COLLECTION VIEW##
    // load TEI content into the output div
    $(document).on('click', '.load-tei-content', loadTEIContent)

    // add a new multi input-field (e.g. 'Basic classification', 'Rights Holder')
    $(document).on('click', '.add-multi-input', addMultiInput);
    // remove a new multi input-field (e.g. 'Basic classification', 'Rights Holder')
    $(document).on('click', '.remove-multi-field', removeMultiInput);
    // save collection settings
    $(document).on('submit', '.collection-form', saveCollectionSettings);

    // load collection tab content
    // Option1: after clicking on the tab
    $(document).on('click', '.collection-tab', loadCollectionTab);
    // Option2: when the page loads (by opening collection in sidebar)
    if ($('.collection-tab.active').length > 0) {
        loadCollectionTab.call($('.collection-tab.active')[0]);
    }

    // ###TEI EXPLORER###
    // load TEI Explorer tab content
    $(document).on(
        'show.bs.tab', 'button[data-bs-toggle="tab"].tei_explorer',
        loadTEIExplorerTab);
    // trigger xpath search
    $(document).on('click', '.check-xpath', checkXPath);
    // show xpath (of a 'dynamic attribute') in TEI Explorer
    $(document).on('click', '.show-xpath-in-tei-explorer', showXPathInTEIExplorer);


    // ##PUBLISH##
    // this is generic form-submit for all forms with class 'tab-submit'
    $(document).on('submit', 'form.tab-submit', tabSubmit);
    // select a listed TextGrid-Project
    $(document).on('click', 'a.select-tg-project', selectTGProject);
    // delete a listed TextGrid-Project
    $(document).on('click', 'a.delete-tg-project', deleteTGProject);

    $('#deleteProject').on('show.bs.modal', function (event) {
        const pressed_button = $(event.relatedTarget);
        const target_input = $(this).find('input[name=projectname]');
        target_input.val(pressed_button.data('projectname'));
    })

    console.log('main.js has been loaded! ');
})