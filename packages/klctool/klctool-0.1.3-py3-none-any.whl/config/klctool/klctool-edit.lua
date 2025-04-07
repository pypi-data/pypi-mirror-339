function Header (el)
    if el.level == 1 then
        return ""
    end
    return nil
end

function Meta (meta)
    meta.title = ""
    return meta
end

return {
    {Header = Header},
    {Meta = Meta},
}
