
// ////////////////////////////////////////////////////////////////////////////
// Globals
// ////////////////////////////////////////////////////////////////////////////

let map;
let api = "http://127.0.0.1:8000";
let INFOS = {
    callbacks: [],
    categories: {},
    points: {},
    parameters: {}
};

// ////////////////////////////////////////////////////////////////////////////
// Events
// ////////////////////////////////////////////////////////////////////////////

/**
 * Lors du chargement de la page
 */
$(document).ready(function () {
    
    // ////////////////////////////////////////////////////
    // Load map

    // map size : 6665x5658
    // A0 : 797.5 1061.4944452102
    // 2193.5 4059.271950379049
    map = L.map('map', {
        crs: L.CRS.Simple,
        minZoom: -4,
        maxZoom: 1
    });
    let bounds = [[0, 0], [708, 1699]];
    let img = L.imageOverlay('/img/map.png', bounds).addTo(map);
    
    map.fitBounds(bounds);
    map.on('click', onMapClick);

    mapLoadCategories();

});

/**
		 * Lors d'un clique sur la carte:
		 * - On affiche un popup permettant la définition des origines
		 * ou
		 * - On rentre les coordonnées dans un champ de texte visible
		 */
function onMapClick(e) {

    let ll = e.latlng

    // Si un champ de texte Position est affiché, on rentre les coordonnées dedans
    $(".pos").val(`${ll.lat|0},${ll.lng|0}`);
        
    // Sinon on affiche le popup pour la définition des origines
    /*else {
        L.popup()
            .setLatLng(ll)
            .setContent(`
                <input type="button" value="Set A0" onclick="setOrigin('A0',${ll.lat|0},${ll.lng|0})">
                <input type="button" value="Set R50" onclick="setOrigin('R50',${ll.lat|0},${ll.lng|0})">
            `)
            .openOn(map);
    }*/

}

/**
 * Lors d'un clique sur un marqueur :
 * - Si un champ de texte Référence
 */
function onMarkerClick(ref) {
    if($(".ref").length > 0) {
        $(".ref").val(`${ref}`);
    }
}


// ////////////////////////////////////////////////////////////////////////////
// Functions
// ////////////////////////////////////////////////////////////////////////////

/**
 * 
 */
 function mapLoadCategories() {

    // Get the categories
    $.get(`${api}/category`)
        .done(function (data) {

            $("select.categories").append(`<option value="">-- Catégorie --</option>`);

            // For each category
            $.each(data["categories"], function(index, cat) {
                // Si la catégorie est inconnue
                if(!(cat["id"] in INFOS.categories)) {

                    let _icon = L.icon({
                        iconUrl: `/img/dot_${cat["color"]}.png`,
                        iconSize:     [10, 10], // size of the icon
                        iconAnchor:   [5, 5], // point of the icon which will correspond to marker's location
                        popupAnchor:  [0, -5] // point from which the popup should open relative to the iconAnchor
                    });

                    // Save categories into dict
                    INFOS.categories[cat["id"]] = {
                        name: cat["name"],
                        icon: _icon
                    };

                    // Add html content
                    $("select.categories").append(`
                        <option value="${cat["id"]}">${cat["name"]}</option>
                    `);
                    $("ul.categories").append(`
                        <li>
                            <img src="/img/dot_${cat["color"]}.png">
                            <input id="cat_${cat["id"]}" type="checkbox" Checked>${cat["name"]}</input>
                        </li>
                    `);
                    $(`#cat_${cat["id"]}`).change(function () {
                        if(this.checked) {
                            $(`.cat_${cat["id"]}`).fadeIn('slow');
                        }
                        else {
                            $(`.cat_${cat["id"]}`).fadeOut('slow');
                        }
                    });
                }
            });

            mapLoadPoints();
        });
}

/**
 * 
 */
function mapLoadPoints() {

    let _select = $(`.point_all`);
    _select.children().remove();
    _select.append(`<option value="">-- Point --</option>`);

    // Get the points
    $.get(`${api}/point/get`)
        .done(function(data) {
            // Pour chaque points
            $.each(data["points"], function(index, point) {
                if(point["id"] in INFOS.points) {
                    INFOS.points[point.id]["x"] = point.x;
                    INFOS.points[point.id]["y"] = point.y;
                }
                else {
                    INFOS.points[point.id] = {
                        category: point.category,
                        x: point.x,
                        y: point.y,
                        marker: null
                    };
                }

                _select.append(`<option>${point.id}</option>`);
            });

            getOrigin();
        });
}

/**
 * Récupère les points d'origines (A0 et R50) de la carte pour le placement des marqueurs
 */
function getOrigin() {
$.get(`${api}/origin`)
    .done(function (data) {
        
        INFOS.parameters["A0"] = data["A0"];
        INFOS.parameters["R50"] = data["R50"];

        $(`.a0`).html(`A0 : ${data["A0"]}`);
        $(`.r50`).html(`R50 : ${data["R50"]}`);

        updateMarker();
    })
    .always(function () {
        if(INFOS.parameters.A0 == undefined || INFOS.parameters.A0 == null ||
            INFOS.parameters.R50 == undefined || INFOS.parameters.R50 == null) {

            $("#map").children(".alert").css("display", "flex");
        }
    });
}

/**
 * Place les marqueurs sur la carte selon les points d'origines
 */
 function updateMarker() {

    // Pour chaque point
    $.each(INFOS.points, function (ref, point) {
        // Calculer la position et afficher le marqueur
        let _A0 = INFOS.parameters.A0;
        let _R50 = INFOS.parameters.R50;
        let lat = (_R50[0] -_A0[0])*point.x +_A0[0];
        let lng = (_R50[1] -_A0[1])*point.y +_A0[1];

        if(point.marker == null) {
            point["marker"] = L.marker([lat|0, lng|0]);
            point["marker"].addTo(map)
                    .bindPopup(ref)
                    .setIcon(INFOS.categories[point.category].icon)
                    .on("click", function(e) {
                        onMarkerClick(ref);
                    });
            $(point["marker"]._icon).addClass(`cat_${point.category}`);
        }
        else {
            point["marker"].setLatLng([lat|0, lng|0]);
        }
    });

    // Tant qu'il y a des choses à mettre à jour
    while(INFOS.callbacks.length > 0) {
        INFOS.callbacks.shift()();
    }
}