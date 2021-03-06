<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output
            method="text"
            version="string"
            encoding="utf-8"
            omit-xml-declaration="yes"
            standalone="yes"
            doctype-public="string"
            doctype-system="string"
            cdata-section-elements="namelist"
            indent="no"
            media-type="string"/>
    <xsl:template match="//enumerated_list">

        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="//enumerated_list">
<xsl:for-each select="list_item">1. <xsl:value-of select="./paragraph/text()"/> <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
