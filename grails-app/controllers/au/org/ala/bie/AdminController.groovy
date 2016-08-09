package au.org.ala.bie
import au.org.ala.web.AlaSecured
import grails.converters.JSON
import grails.converters.XML

@AlaSecured(value = "ROLE_ADMIN", redirectUri = "/")
class AdminController {

    def index() {
        redirect(controller: "alaAdmin")
    }

    def indexFields() {
        redirect(controller: "misc", action: "indexFields") // shouldn't get triggered due UrlMappings
    }
}
